import cv2
import pyautogui
import time
import numpy as np

def calculate():
    time.sleep(2)
    print("*********************************")
    print("<<<----Take cursor top left---->>>")
    time.sleep(2)
    print("---First Coordinate SUCCESS---")
    point1 = pyautogui.position()
    print("<<<----Take cursor second position---->>>")
    time.sleep(2)
    point2 = pyautogui.position()
    print("---Second Coordinate SUCCESS---")
    print("*********************************")
    region = (point1.x,point1.y,point2.x-point1.x,point2.y-point1.y)
    return region

def screenshot(region):
    im = pyautogui.screenshot(region=region)
    screenshot_np = np.array(im)
    screenshot_np = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2BGR)
    gray_screenshot = cv2.cvtColor(screenshot_np, cv2.COLOR_BGR2GRAY)
    return gray_screenshot

def main():
    deneme = 0
    answers_yes = ["yes", "y"]
    
    cv2.namedWindow("frame")

    while(True):
        print("Taking question coordinates")
        main_region_coord = calculate()
        main_region = screenshot(main_region_coord)
        cv2.imshow('frame', main_region)
        k = cv2.waitKey(0)
        cv2.destroyWindow('frame')
        cv2.waitKey(1)
        if k == ord('y'):
            break
    
    count = int(input("how many screenshot?"))
    regions = []
    for i in range(count):
        while True:
            region = calculate()
            gray_screenshot = screenshot(region)
            cv2.imshow('frame', gray_screenshot)
            k = cv2.waitKey(0)
            cv2.destroyWindow('frame')
            cv2.waitKey(1)
            if k == ord('y'):
                regions.append(gray_screenshot)
                break
    while True:
        time.sleep(3)
        found = True
        count = 0
        main_region = screenshot(main_region_coord)
        for region in regions:
            result = cv2.matchTemplate(main_region, gray_screenshot, cv2.TM_CCOEFF_NORMED)
            _, max_val, _, _ = cv2.minMaxLoc(result)
            count += 1
            if not max_val>.985:
                deneme += 1
                print(f"Try {deneme} has failed..{count} of {len(regions)}, {max_val}")
                found = False
                break
        if found:
            print("------------------------")
            answer = input("Did you find? ")
            if answer in answers_yes:
                break
            else:
                time.sleep(1)
        pyautogui.click(button='left')

if __name__=="__main__":
    main()
    