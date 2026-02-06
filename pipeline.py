"""
End-to-end pipeline orchestration for COREP reporting.
"""
from typing import List, Optional

from models.regulatory import RegulatoryChunk
from models.corep import CorepOutput, OwnFunds, FieldJustification
from knowledge_base import get_all_chunks
from retrieval import EmbeddingGenerator, VectorStore
from reasoning import LLMClient, build_system_prompt, build_user_prompt
from validation import Validator
import config


class CorepPipeline:
    """Orchestrates the full COREP reporting pipeline."""
    
    def __init__(self):
        """Initialize pipeline components."""
        self.embedding_generator = EmbeddingGenerator()
        self.vector_store = VectorStore(self.embedding_generator)
        self.llm_client = LLMClient()
        self.validator = Validator()
        self._index_built = False
    
    def _ensure_index(self) -> None:
        """Build vector index if not already built."""
        if not self._index_built:
            chunks = get_all_chunks()
            print(f"📚 Building index from {len(chunks)} regulatory chunks...")
            self.vector_store.build_index(chunks)
            self._index_built = True
            print("✅ Index built successfully\n")
    
    def retrieve_chunks(
        self, 
        question: str, 
        top_k: int = None
    ) -> List[RegulatoryChunk]:
        """
        Retrieve relevant regulatory chunks for a question.
        
        Args:
            question: User's natural language question
            top_k: Number of chunks to retrieve
            
        Returns:
            List of relevant RegulatoryChunk objects
        """
        self._ensure_index()
        
        top_k = top_k or config.TOP_K_CHUNKS
        results = self.vector_store.retrieve(question, top_k)
        
        print(f"🔍 Retrieved {len(results)} relevant regulatory chunks:")
        for chunk, distance in results:
            print(f"   - {chunk.id}: {chunk.source}, {chunk.paragraph} (dist: {distance:.4f})")
        print()
        
        return [chunk for chunk, _ in results]
    
    def reason_with_llm(
        self, 
        question: str, 
        chunks: List[RegulatoryChunk]
    ) -> Optional[dict]:
        """
        Use LLM to interpret rules and generate COREP output.
        
        Args:
            question: User's question
            chunks: Retrieved regulatory chunks
            
        Returns:
            Parsed JSON response or None
        """
        print("🤖 Calling LLM for regulatory interpretation...")
        
        system_prompt = build_system_prompt()
        user_prompt = build_user_prompt(question, chunks)
        
        response = self.llm_client.generate_json(system_prompt, user_prompt)
        
        if response:
            print("✅ LLM response received and parsed\n")
        else:
            print("❌ Failed to parse LLM response\n")
        
        return response
    
    def validate_and_build_output(self, raw_output: dict) -> CorepOutput:
        """
        Validate raw LLM output and build CorepOutput.
        
        Args:
            raw_output: Parsed JSON from LLM
            
        Returns:
            Validated CorepOutput with warnings
        """
        print("✔️  Validating output...")
        
        # Build OwnFunds
        own_funds_data = raw_output.get("own_funds", {})
        own_funds = OwnFunds(
            common_equity_tier_1=own_funds_data.get("common_equity_tier_1", 0),
            additional_tier_1=own_funds_data.get("additional_tier_1", 0),
            tier_2=own_funds_data.get("tier_2", 0),
            total_own_funds=own_funds_data.get("total_own_funds", 0)
        )
        
        # Build audit log
        audit_log = []
        for entry in raw_output.get("audit_log", []):
            audit_log.append(FieldJustification(
                field=entry.get("field", "unknown"),
                value=entry.get("value", 0),
                rule_ids=entry.get("rule_ids", []),
                explanation=entry.get("explanation", "No explanation provided")
            ))
        
        # Build initial output
        output = CorepOutput(
            own_funds=own_funds,
            audit_log=audit_log,
            warnings=raw_output.get("warnings", [])
        )
        
        # Run validations
        validation_warnings = self.validator.run_all_validations(output)
        
        # Add validation warnings to output
        output.warnings.extend(validation_warnings)
        
        if validation_warnings:
            print(f"⚠️  {len(validation_warnings)} validation warning(s) found\n")
        else:
            print("✅ All validations passed\n")
        
        return output
    
    def run(self, question: str) -> CorepOutput:
        """
        Run the full COREP reporting pipeline.
        
        Args:
            question: User's natural language question
            
        Returns:
            Complete, validated CorepOutput
        """
        print("=" * 60)
        print("🚀 STARTING COREP REPORTING PIPELINE")
        print("=" * 60)
        print(f"\n📝 Question: {question}\n")
        
        # Step 1: Retrieve relevant chunks
        chunks = self.retrieve_chunks(question)
        
        # Step 2: LLM reasoning
        raw_output = self.reason_with_llm(question, chunks)
        
        if raw_output is None:
            raise ValueError("LLM failed to generate valid output")
        
        # Step 3: Validate and build output
        output = self.validate_and_build_output(raw_output)
        
        print("=" * 60)
        print("✅ PIPELINE COMPLETE")
        print("=" * 60 + "\n")
        
        return output
