import logging
import os

from huggingface_hub import snapshot_download
from fiftyone.operators import types

# Import constants from zoo.py to ensure consistency
from .zoo import QWEN_OPERATIONS, QwenModel

logger = logging.getLogger(__name__)

def download_model(model_name, model_path):
    """Downloads the model.

    Args:
        model_name: the name of the model to download, as declared by the
            ``base_name`` and optional ``version`` fields of the manifest
        model_path: the absolute filename or directory to which to download the
            model, as declared by the ``base_filename`` field of the manifest
    """
    
    snapshot_download(repo_id=model_name, local_dir=model_path)

def load_model(model_name, model_path, **kwargs):
    """Loads the model.

    Args:
        model_name: the name of the model to load, as declared by the
            ``base_name`` and optional ``version`` fields of the manifest
        model_path: the absolute filename or directory to which the model was
            donwloaded, as declared by the ``base_filename`` field of the
            manifest
        **kwargs: optional keyword arguments that configure how the model
            is loaded

    Returns:
        a :class:`fiftyone.core.models.Model`
    """
    # Import QwenModel from zoo.py
    from .zoo import QwenModel
    
    if not model_path or not os.path.isdir(model_path):
        raise ValueError(
            f"Invalid model_path: '{model_path}'. Please ensure the model has been downloaded "
            "using fiftyone.zoo.download_zoo_model(...)"
        )
    
    logger.info(f"Loading QwenModel model from {model_path}")

    # Create and return the model - operations specified at apply time
    return QwenModel(model_path=model_path, **kwargs)


def resolve_input(model_name, ctx):
    """Defines properties to collect the model's custom parameters.

    Args:
        model_name: the name of the model
        ctx: an ExecutionContext

    Returns:
        a fiftyone.operators.types.Property
    """

    inputs = types.Object()
    
    # Operation selection
    inputs.enum(
        "operation",
        values=list(QWEN_OPERATIONS.keys()),
        default=None,
        required=True,
        label="Operation",
        description="Type of task to perform with Qwen2.5-VL model",
        view=types.AutocompleteView()
    )
    
    inputs.str(
        "system_prompt",
        default=None,
        required=False,
        label="System Prompt",
        description="Optional custom system prompt",
        view=types.AutocompleteView()
    )
    
    inputs.str(
        "prompt",
        default=None,
        required=False,
        label="Prompt",
        description="Prompt for guiding operation",
        view=types.AutocompleteView()
    )
    
    return types.Property(inputs)


# def parse_parameters(model_name, ctx, params):
#     """Processes and validates the model's custom parameters.

#     Args:
#         model_name: the name of the model
#         ctx: an ExecutionContext
#         params: a params dict
        
#     Raises:
#         ValueError: If required parameters are missing
#     """
#     # Ensure operation is specified
#     if "operation" not in params:
#         raise ValueError("Operation must be specified")
        
#     operation = params["operation"]
    
#     # Validate required parameters for specific operations
#     if operation == "phrase_grounding":
#         if not params.get("caption") and not params.get("caption_field"):
#             raise ValueError("Either 'caption' or 'caption_field' must be provided for phrase grounding")
            
#         # If both are provided, raise an error
#         if params.get("caption") and params.get("caption_field"):
#             raise ValueError("Only ONE of 'caption' or 'caption_field' can be provided for phrase grounding")
            
#     if operation == "segmentation":
#         if not params.get("expression") and not params.get("expression_field"):
#             raise ValueError("Either 'expression' or 'expression_field' must be provided for segmentation")
            
#         # If both are provided, prefer expression over expression_field  
#         if params.get("expression") and params.get("expression_field"):
#             raise ValueError("Only ONE of 'expression' or 'expression_field' can be provided for segmentation")