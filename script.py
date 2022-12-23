import cv2
import PySimpleGUI as sg

def checkCameras() -> list[int]:
  """
    Searches for all open camera ports
  """
  is_working = True
  dev_port = 0
  working_ports = []
  while is_working:
    camera = cv2.VideoCapture(dev_port)
    if not camera.isOpened():
      is_working = False
    else:
      is_reading = camera.read()
      if is_reading:
        working_ports.append(dev_port)
    dev_port +=1
  return working_ports

def Main():
  workingPorts = checkCameras()
  letters = [" ", ".", "'", ",", ":", "^", ";", "-", "+", "*", "=", "O", "0", "%", "$", "§", "?", "#"]

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
      ),
      sg.Combo(
        workingPorts,
        default_value=0,
        background_color="black",
        text_color="white",
        button_background_color="black",
        button_arrow_color="white",
        change_submits=True,
        key="-ACTIVECAMERA-",
        font="Arial 12"
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
        output += letters[pixels // 15]
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

    if event == "-ACTIVECAMERA-":
      try: 
        cam = cv2.VideoCapture(values["-ACTIVECAMERA-"])
      except: 
        cam = cv2.VideoCapture(0)

    if values["-CAMERAACTIV-"]:

      ret, frame = cam.read()
      text = renderText(frame)

      window["-TEXT-"].update(text)
  window.close()

if __name__ == "__main__":
  Main()