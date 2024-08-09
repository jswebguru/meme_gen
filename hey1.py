import requests
import cv2


BRAND_PATH = 'input/download.jpg'
def generate_meme(prompt):
    response = requests.post(
        f"https://api.stability.ai/v2beta/stable-image/generate/ultra",
        headers={
            "authorization": f"Bearer sk-RzQ14qMtrmvn6LfVkjcLzE5HKDusntYB3gUkMNPJBowhsA5A",
            "accept": "image/*"
        },
        files={"none": ''},
        data={
            "prompt": prompt + " That's a meme image and without any description indicates it's a meme",
            "output_format": "webp",
        },
    )

    if response.status_code == 200:
        with open("input/handle.webp", 'wb') as file:
            file.write(response.content)
    else:
        raise Exception(str(response.json()))
    return response.content

def add_branding(webp_image_path):
    image = cv2.imread(webp_image_path, cv2.IMREAD_UNCHANGED)
    brand_img = cv2.imread(BRAND_PATH, cv2.IMREAD_UNCHANGED)
    brand_h, brand_w = brand_img.shape[:2]

    img_h, img_w = image.shape[:2]

    # Ensure the brand image fits into the main image
    if brand_w > img_w:
        brand_w = img_w
        brand_img = cv2.resize(brand_img, (brand_w, int(brand_h * img_w / brand_w)), interpolation=cv2.INTER_AREA)
        brand_h = brand_img.shape[0]

        # Position at the bottom-right corner
    overlay_position = (img_h - brand_h, img_w - brand_w)

    # Handling transparency
    if len(brand_img.shape) == 3 and brand_img.shape[2] == 4:
        # Split out the transparency mask from the color info
        alpha_brand = brand_img[:, :, 3] / 255.0
        alpha_image = 1.0 - alpha_brand

        for c in range(0, 3):
            image[overlay_position[0]:overlay_position[0] + brand_h,
            overlay_position[1]:overlay_position[1] + brand_w, c] = (
                    alpha_brand * brand_img[:, :, c] +
                    alpha_image * image[overlay_position[0]:overlay_position[0] + brand_h,
                                  overlay_position[1]:overlay_position[1] + brand_w, c])
    else:
        image[overlay_position[0]:overlay_position[0] + brand_h,
        overlay_position[1]:overlay_position[1] + brand_w] = brand_img

    return image
def save_image(image, output_path):
    cv2.imwrite(output_path, image)

def main():
    prompt = input("Enter a prompt for the meme: ")

    meme_image = generate_meme(prompt)
    if meme_image is not None:
        meme_with_branding = add_branding('input/handle.webp')
        output_path = 'result/generated_meme.png'
        save_image(meme_with_branding, output_path)
        print(f"Meme generated and saved to {output_path}")
    else:
        print("Could not generate the meme.")


if __name__ == "__main__":
    main()