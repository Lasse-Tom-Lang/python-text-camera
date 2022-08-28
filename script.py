import cv2
import PySimpleGUI as sg

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


while True:
  event, values = window.read((1000 / 60))
  if event == sg.WIN_CLOSED:
    break

  if values["-CAMERAACTIV-"]:

    ret, frame = cam.read()

    image = cv2.resize(
      frame,
      (
        frame.shape[1] // 6,
        frame.shape[0] // 10
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
        if pixels > 0 and pixels < 20:
          output += "."
        if pixels > 20 and pixels < 40:
          output += ","
        if pixels > 40 and pixels < 60:
          output += ":"
        if pixels > 60 and pixels < 80:
          output += ";"
        if pixels > 80 and pixels < 100:
          output += "-"
        if pixels > 100 and pixels < 120:
          output += "+"
        if pixels > 120 and pixels < 140:
          output += "*"
        if pixels > 140 and pixels < 160:
          output += "%"
        if pixels > 160 and pixels < 180:
          output += "$"
        if pixels > 180 and pixels < 200:
          output += "§"
        if pixels > 200 and pixels < 220:
          output += "?"
        if pixels > 220 and pixels < 240:
          output += "="
        if pixels > 240:
          output += "#"
      imageChars += output + "\n"
    window["-TEXT-"].update(imageChars)
window.close()