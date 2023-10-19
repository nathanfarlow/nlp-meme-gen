import argparse
import config
from PIL import Image
import cv2
import shutil


def is_video(filename):
    ext = filename.split(".")[-1]
    return ext in {
        "mp4",
        "gif",
        "webm",
        "mov",
        "avi",
        "mkv",
        "flv",
        "wmv",
        "m4v",
        "m4p",
        "m4b",
    }


def crop(image):
    print("Crop image.")

    r = cv2.selectROI(image)
    if r[2] == 0 or r[3] == 0:
        print("Ok, skipping cropping.")
        cropped = image
    else:
        cropped = image[int(r[1]) : int(r[1] + r[3]), int(r[0]) : int(r[0] + r[2])]
    cv2.destroyAllWindows()
    return cropped


def read_four_points(image) -> config.SkewedRectangle:
    print("Select 4 points in order: top left, top right, bottom right, bottom left")
    print("Press enter to save, any thing else to retry")
    while True:
        control_points = []

        tmp_image = image.copy()

        def mouse_callback(event, x, y, *_):
            if event == cv2.EVENT_LBUTTONDOWN and len(control_points) < 4:
                if len(control_points) > 0:
                    cv2.line(
                        tmp_image,
                        control_points[-1],
                        (x, y),
                        (0, 0, 255),
                        thickness=2,
                    )
                if len(control_points) == 3:
                    cv2.line(
                        tmp_image,
                        control_points[0],
                        (x, y),
                        (0, 0, 255),
                        thickness=2,
                    )
                control_points.append((x, y))
                cv2.circle(tmp_image, (x, y), 2, (0, 0, 255), -1)
                cv2.imshow("Select text region", tmp_image)

        cv2.imshow("Select text region", tmp_image)
        cv2.setMouseCallback("Select text region", mouse_callback)

        if cv2.waitKey(0) != 13:
            print("Retrying")
            continue

        cv2.destroyAllWindows()

        if len(control_points) != 4:
            print("You must select exactly 4 points.")
            continue
        else:
            return (
                control_points[0],
                control_points[1],
                control_points[2],
                control_points[3],
            )


def read_bounds(image) -> config.SkewedRectangle:
    while True:
        response = input("Rectangle (r) or skewed (s)? ")
        if response.startswith("r"):
            r = cv2.selectROI(image)
            if r[2] == 0 or r[3] == 0:
                print("Retrying")
                continue
            cv2.destroyAllWindows()
            return (
                (r[0], r[1]),
                (r[0] + r[2], r[1]),
                (r[0] + r[2], r[1] + r[3]),
                (r[0], r[1] + r[3]),
            )
        elif response.startswith("s"):
            return read_four_points(image)
        else:
            print("invalid response")


def read_font():
    while True:
        response = input("Arial (a) or impact (i)? ").lower()
        if response.startswith("a"):
            return config.Font.ARIAL
        elif response.startswith("i"):
            return config.Font.IMPACT
        else:
            print("invalid response")


def read_all_text_boxes(image) -> list[config.TextBox]:
    text_boxes = []
    while True:
        response = input("Add a text box? (y/n) ").lower()
        if response.startswith("y"):
            font = read_font()
            tag = input("Tag: ")
            bounds = read_bounds(image)
            text_boxes.append(config.TextBox(bounds=bounds, font=font, tag=tag))
        elif response.startswith("n"):
            return text_boxes
        else:
            print("invalid response")


def read_description():
    return input("Description: (add as many tags and details as you can) ")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--in-template", type=str, required=True)
    parser.add_argument("--out-template", type=str, required=True)
    parser.add_argument("--in-config", type=str, required=False)
    parser.add_argument("--out-config", type=str, required=False)

    args = parser.parse_args()

    if args.in_config is None:
        meme_conf = config.Config(memes=[])
    else:
        meme_conf = config.load(args.in_config)

    description = read_description()
    if not is_video(args.in_template):
        image = cv2.imread(args.in_template)
        image = crop(image)
        cv2.imwrite(args.out_template, image)
        textboxes = read_all_text_boxes(image)
    else:
        textboxes = []
        shutil.copyfile(args.in_template, args.out_template)

    meme = config.Meme(
        description=description,
        filepath=args.out_template,
        textboxes=textboxes,
    )

    meme_conf.memes.append(meme)

    if args.out_config is None:
        print(meme_conf.to_json())
    else:
        print(f"Saving updated config to {args.out_config}")
        meme_conf.save(args.out_config)


if __name__ == "__main__":
    main()
