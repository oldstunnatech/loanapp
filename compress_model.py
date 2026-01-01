import joblib
import os

# Path to your current large model
# This path is relative to the root of your project folder
model_path = 'transactionapp/ML_models/xgb_model.pkl'

def compress_model():
    if os.path.exists(model_path):
        initial_size = os.path.getsize(model_path) / (1024 * 1024)
        print(f"--- Model Compression Tool ---")
        print(f"Current model found at: {model_path}")
        print(f"Initial file size: {initial_size:.2f} MB")
        
        print("\nLoading model into memory (this may take a moment)...")
        try:
            model = joblib.load(model_path)
            
            # Save with compression level 3
            # 'compress=3' is a good balance between compression ratio and speed
            print("Compressing and overwriting original file...")
            joblib.dump(model, model_path, compress=3)
            
            new_size = os.path.getsize(model_path) / (1024 * 1024)
            reduction = ((initial_size - new_size) / initial_size) * 100
            
            print(f"\nSuccess!")
            print(f"New file size: {new_size:.2f} MB")
            print(f"Reduction: {reduction:.1f}%")
            print("\nYou can now proceed with: git add, git commit, and git push.")
            
        except Exception as e:
            print(f"Error during compression: {e}")
    else:
        print(f"Error: Model file not found at {model_path}")
        print("Please check the folder structure: transactionapp/ML_models/")

if __name__ == "__main__":
    compress_model()