import logging
import os

from huggingface_hub import snapshot_download
from fiftyone.operators import types

# Import constants from zoo.py to ensure consistency
from .zoo import SYSTEM_PROMPTS, QwenModel

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
        values=list(SYSTEM_PROMPTS.keys()),
        default=None,
        required=True,
        label="Operation",
        description="Type of task to perform with Florence2 model",
        view=types.AutocompleteView()
    )
    
    # Caption detail level
    inputs.enum(
        "detail_level",
        values=["basic", "detailed", "more_detailed"],
        default=None,
        required=False,
        label="Caption detail level",
        description="Level of detail in generated captions",
        view=types.AutocompleteView(),
    )
    
    # OCR parameters
    inputs.bool(
        "store_region_info",
        default=None,
        required=False,
        label="Store region information",
        description="Whether to include text region bounding boxes",
        view=types.AutocompleteView()
    )
    
    # Detection parameters
    inputs.enum(
        "detection_type",
        options=["detection", "dense_region_caption", "region_proposal", "open_vocabulary_detection"],
        default=None,
        required=False,
        label="Detection type",
        description="Type of detection to perform",
        view=types.AutocompleteView()
    )
    
    inputs.str(
        "text_prompt",
        default=None,
        required=False,
        label="Text prompt",
        description="Optional prompt for guiding detection (Florence2 only supports one class prompt)",
        view=types.AutocompleteView()
    )
    
    # Phrase grounding parameters
    inputs.str(
        "caption",
        default=None,
        required=False,
        label="Caption",
        description="Caption text to ground in the image",
        view=types.AutocompleteView()
    )
    
    inputs.str(
        "caption_field",
        default=None,
        required=False,
        label="Caption field",
        description="Name of the sample field containing caption to ground",
        view=types.AutocompleteView()
    )
    
    # Segmentation parameters
    inputs.str(
        "expression",
        default=None,
        required=False,
        label="Expression",
        description="Natural language expression describing the object to segment",
        view=types.AutocompleteView()
    )
    
    inputs.str(
        "expression_field",
        default=None,
        required=False,
        label="Expression field",
        description="Name of the sample field containing the expression",
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