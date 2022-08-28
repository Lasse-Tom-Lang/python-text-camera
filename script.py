import cv2
import PySimpleGUI as sg

letters = [".", ",", ":", ";", "-", "+", "*", "%", "$", "§", "?", "=", "#"]

layout = [
  [
    sg.Multiline(
      expand_x=True,
      expand_y=True,
      key="-TEXT-",
      background_color="black",
      text_color="white",
      no_scrollbar=True,
      font=("Andale Mono", 10),
      border_width=0
    )
  ],
  [
    sg.Checkbox(
      "Camera activ",
      key="-CAMERAACTIV-",
      background_color="black",
      text_color="white",
      font="Arial 16",
      default=True
    ),
    sg.FileBrowse(
      "Select image",
      target="-SELECTEDIMAGE-",
      button_color=("white", "black")
    ),
    sg.In(
      key="-SELECTEDIMAGE-",
      change_submits=True,
      visible=False
    ),
    sg.Slider(
      (40, 300),
      key="-IMAGEWIDTH-",
      default_value=200,
      orientation="horizontal",
      disable_number_display=True,
      background_color="black",
      trough_color="white"
    ),
    sg.Slider(
      (40, 300),
      key="-IMAGEHEIGHT-",
      default_value=68,
      orientation="horizontal",
      disable_number_display=True,
      background_color="black",
      trough_color="white"
    )
  ]
]

window = sg.Window(
  "Test",
  layout,
  resizable=True,
  background_color="black"
)

window.read(1)

window.Maximize()

cam = cv2.VideoCapture(0)

def renderText(image):
  image = cv2.resize(
    image,
    (
      frame.shape[1] // (frame.shape[1] // int(values["-IMAGEWIDTH-"])),
      frame.shape[0] // (frame.shape[0] // int(values["-IMAGEHEIGHT-"]))
    )
  )
  imageGray = cv2.cvtColor(
    image,
    cv2.COLOR_BGR2GRAY
  )

  imageChars = ""

  for lines in imageGray:
    output = ""
    for pixels in lines:
      output += letters[pixels // 20]
    imageChars += output + "\n"
  return imageChars


while True:
  event, values = window.read((1000 / 60))
  if event == sg.WIN_CLOSED:
    break

  if event == "-SELECTEDIMAGE-":
    try:
      loadedImage = cv2.imread(values["-SELECTEDIMAGE-"])
      text = renderText(loadedImage)

      window["-TEXT-"].update(text)
    except:
      continue

  if values["-CAMERAACTIV-"]:

    ret, frame = cam.read()
    text = renderText(frame)

    window["-TEXT-"].update(text)
window.close()