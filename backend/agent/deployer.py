"""
Deployer Module - Handles automatic deployment to Vercel.
"""
import os
import subprocess
import json

def deploy_to_vercel(project_path: str = "output"):
    """
    Deploys the generated project to Vercel.
    Requires Vercel CLI installed and authenticated.
    
    Returns deployment URL or error message.
    """
    result = {
        "success": False,
        "url": None,
        "message": ""
    }
    
    # Check if Vercel CLI is available
    try:
        version_check = subprocess.run(
            ["vercel", "--version"],
            capture_output=True,
            text=True,
            timeout=10
        )
        if version_check.returncode != 0:
            result["message"] = "Vercel CLI not installed. Run: npm i -g vercel"
            return result
    except FileNotFoundError:
        result["message"] = "Vercel CLI not found. Run: npm i -g vercel"
        return result
    except Exception as e:
        result["message"] = f"Error checking Vercel: {str(e)}"
        return result
    
    # Deploy the project
    try:
        deploy_result = subprocess.run(
            ["vercel", "--yes", "--prod"],
            cwd=project_path,
            capture_output=True,
            text=True,
            timeout=120
        )
        
        if deploy_result.returncode == 0:
            # Extract URL from output
            output_lines = deploy_result.stdout.strip().split("\n")
            for line in output_lines:
                if "https://" in line:
                    result["url"] = line.strip()
                    result["success"] = True
                    result["message"] = "Deployed successfully!"
                    break
            if not result["url"]:
                result["success"] = True
                result["message"] = "Deployed, but couldn't extract URL."
        else:
            result["message"] = f"Deploy failed: {deploy_result.stderr}"
            
    except subprocess.TimeoutExpired:
        result["message"] = "Deployment timed out."
    except Exception as e:
        result["message"] = f"Deploy error: {str(e)}"
    
    return result

def mock_deploy(project_path: str = "output"):
    """
    Simulates deployment for demo purposes.
    """
    return {
        "success": True,
        "url": f"https://autogenesis-demo.vercel.app/{os.path.basename(project_path)}",
        "message": "Mock deployment successful (Vercel CLI not configured)."
    }

def smart_deploy(project_path: str = "output"):
    """
    Attempts real deployment, falls back to mock.
    """
    real_result = deploy_to_vercel(project_path)
    if real_result["success"]:
        return real_result
    
    # Fallback to mock
    mock_result = mock_deploy(project_path)
    mock_result["message"] += f" (Real deploy failed: {real_result['message']})"
    return mock_result
