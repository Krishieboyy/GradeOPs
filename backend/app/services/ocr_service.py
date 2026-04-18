import torch
from app.models.loader import model, processor, device
from app.config import MAX_NEW_TOKENS

def extract_text_from_image(image):
    conversation = [
        {
            "role": "user",
            "content": [
                {"type": "image"},
                {
                    "text": """You are an OCR system.
                    Extract text EXACTLY as written in the image.

                    Rules:
                    - Do NOT explain anything
                    - Do NOT correct grammar or facts   
                    - Do NOT add missing information
                    - Do NOT summarize
                    - Keep original formatting as much as possible
                    - If something is unreadable, write [unclear]

                    Only output the raw extracted text."""
                }
            ]
        }
    ]

    text_prompt = processor.apply_chat_template(
        conversation,
        add_generation_prompt=True
    )

    inputs = processor(
        text=[text_prompt],
        images=[image],
        padding=True,
        return_tensors="pt"
    )

    inputs = {k: v.to(device) for k, v in inputs.items()}

    with torch.no_grad():
        output_ids = model.generate(**inputs, max_new_tokens=MAX_NEW_TOKENS)

    generated_ids = [
        output_ids[i][len(inputs["input_ids"][i]):]
        for i in range(len(output_ids))
    ]

    output_text = processor.batch_decode(
        generated_ids,
        skip_special_tokens=True,
        clean_up_tokenization_spaces=True
    )

    return output_text[0]