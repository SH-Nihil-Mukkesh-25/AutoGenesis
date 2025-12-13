"""
Oumi RL Fine-Tuning Integration for Autogenesis.
Uses Oumi's Reinforcement Learning to improve code generation quality.

This script demonstrates how Autogenesis would use Oumi for:
1. Collecting (code, feedback) pairs from user ratings
2. Training a reward model based on user preferences
3. Fine-tuning the code generator with RLHF

Note: Requires `pip install oumi` (optional, graceful fallback)
"""
import json
import os
from pathlib import Path

# Storage paths
FEEDBACK_FILE = Path("storage/feedback.json")
CHECKPOINTS_DIR = Path("storage/oumi_checkpoints")

def collect_feedback(code: str, rating: int, idea: str):
    """
    Collect user feedback on generated code.
    Rating: 1-5 stars
    """
    FEEDBACK_FILE.parent.mkdir(exist_ok=True)
    
    feedback = []
    if FEEDBACK_FILE.exists():
        feedback = json.loads(FEEDBACK_FILE.read_text())
    
    feedback.append({
        "idea": idea,
        "code": code[:1000],  # Truncate for storage
        "rating": rating,
        "is_positive": rating >= 4
    })
    
    FEEDBACK_FILE.write_text(json.dumps(feedback, indent=2))
    print(f"✅ Feedback collected: {rating}/5 stars")
    return len(feedback)

def prepare_rl_dataset():
    """
    Prepare dataset for Oumi RL training.
    Creates (prompt, chosen, rejected) triplets.
    """
    if not FEEDBACK_FILE.exists():
        print("No feedback data yet")
        return []
    
    feedback = json.loads(FEEDBACK_FILE.read_text())
    
    # Sort into positive/negative examples
    positive = [f for f in feedback if f['is_positive']]
    negative = [f for f in feedback if not f['is_positive']]
    
    # Create preference pairs
    pairs = []
    for pos in positive:
        for neg in negative:
            if pos['idea'].lower()[:20] == neg['idea'].lower()[:20]:
                pairs.append({
                    "prompt": f"Generate code for: {pos['idea']}",
                    "chosen": pos['code'],
                    "rejected": neg['code']
                })
    
    print(f"📊 Created {len(pairs)} preference pairs for RL training")
    return pairs

def train_with_oumi():
    """
    Fine-tune using Oumi's RL capabilities.
    This demonstrates the integration pattern.
    """
    try:
        from oumi import Oumi
        from oumi.core.configs import TrainingConfig
        from oumi.core.trainers import RLTrainer
        
        print("🚀 Starting Oumi RL fine-tuning...")
        
        # Prepare data
        pairs = prepare_rl_dataset()
        if not pairs:
            print("Need at least one preference pair to train")
            return
        
        # Configure training
        config = TrainingConfig(
            model_name="meta-llama/Llama-2-7b-hf",
            learning_rate=1e-5,
            num_epochs=1,
            batch_size=4,
            method="dpo"  # Direct Preference Optimization
        )
        
        # Initialize trainer
        trainer = RLTrainer(config)
        
        # Train
        CHECKPOINTS_DIR.mkdir(exist_ok=True)
        trainer.train(pairs, output_dir=str(CHECKPOINTS_DIR))
        
        print(f"✅ Model fine-tuned and saved to {CHECKPOINTS_DIR}")
        
    except ImportError:
        print("⚠️  Oumi not installed. Using demo mode.")
        print("   To install: pip install oumi")
        print("")
        print("   Demo: Would train on these preference pairs:")
        pairs = prepare_rl_dataset()
        for p in pairs[:3]:
            print(f"   - Prompt: {p['prompt'][:40]}...")

def get_rl_stats():
    """Get current RL training stats."""
    stats = {
        "feedback_count": 0,
        "positive_examples": 0,
        "negative_examples": 0,
        "model_checkpoints": 0
    }
    
    if FEEDBACK_FILE.exists():
        feedback = json.loads(FEEDBACK_FILE.read_text())
        stats["feedback_count"] = len(feedback)
        stats["positive_examples"] = sum(1 for f in feedback if f['is_positive'])
        stats["negative_examples"] = stats["feedback_count"] - stats["positive_examples"]
    
    if CHECKPOINTS_DIR.exists():
        stats["model_checkpoints"] = len(list(CHECKPOINTS_DIR.glob("*")))
    
    return stats

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "train":
            train_with_oumi()
        elif sys.argv[1] == "stats":
            stats = get_rl_stats()
            print("📊 Oumi RL Stats:")
            for k, v in stats.items():
                print(f"   {k}: {v}")
        elif sys.argv[1] == "feedback" and len(sys.argv) >= 4:
            collect_feedback(sys.argv[2], int(sys.argv[3]), sys.argv[4] if len(sys.argv) > 4 else "")
    else:
        print("Autogenesis Oumi RL Integration")
        print("Usage:")
        print("  python oumi_rl.py train      - Train with collected feedback")
        print("  python oumi_rl.py stats      - Show RL training stats")
        print("  python oumi_rl.py feedback <code> <rating> <idea>")
