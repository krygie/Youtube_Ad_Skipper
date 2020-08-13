import pyautogui as pag
import time


class SkipBot:
    num_video_ads_skipped = 0
    num_banners_closed = 0
    width = None
    height = None
    searching_confidence = 0.7  # Should be tweaked for optimal performance. 0.7 is a good starting value.
    movement_delay_s = 0.5
    screen_distance_tolerance = 5
    pause_region_rel = (0, 0.9, 0.1, 0.1)  # left, top, width, height in relative screen units
    skip_ad_region_rel = (0.8, 0.6, 0.2, 0.3)  # same as above
    banner_x_region_rel = (0.6, 0.6, 0.3, 0.3)  # same as above
    pause_region_pixels = None
    skip_ad_region_pixels = None
    banner_x_region_pixels = None

    # Images - these should be replaced when being used for the first time
    play_img = 'play_button.png'  # Picture of the play button when the video is paused
    skip_img = 'skip_ad_button.png'  # Picture of the "Skip" in the Skip Ad(s) button
    x_white_img = 'x_banner_white.png'  # Picture of the white square with a black "x" of a banner ad

    def __init__(self):
        # Get monitor info
        self.width, self.height = pag.size()

        # Wait for the user to setup the video
        pag.alert(text=("Setup Youtube in full-screen mode, press play and then move your mouse to the top of the "
                        "screen (avoid the corners!)."), title="User input needed", button="I understand")
        while True:
            _, mouse_y = pag.position()
            # Break once the mouse is near the top of the screen
            if mouse_y < (0+self.screen_distance_tolerance):
                break

        # Convert relative screen regions into absolute screen regions
        self.pause_region_pixels = SkipBot.region_rel_to_abs(self.pause_region_rel, self.width, self.height)
        self.skip_ad_region_pixels = SkipBot.region_rel_to_abs(self.skip_ad_region_rel, self.width, self.height)
        self.banner_x_region_pixels = SkipBot.region_rel_to_abs(self.banner_x_region_rel, self.width, self.height)

        print("Setup complete!")

        self.activate_the_bot()

        pag.alert(text=(f"I skipped {self.num_video_ads_skipped} video ads and closed {self.num_banners_closed} banner "
                        "ads! Thanks for using me :)"),
                  title="SkipBot deactivated")

    def activate_the_bot(self):
        _, mouse_y = pag.position()

        pag.alert(text="Bot armed!!! To turn off the bot, move the mouse to the bottom of the screen.",
                  title="Bot armed")

        # Bot duties
        while mouse_y <= (self.height-self.screen_distance_tolerance):
            banner_target = self.find_img_center(self.x_white_img, self.banner_x_region_pixels)
            # This can be built upon to also close the black banner ad variants

            if banner_target is not None:
                self.click_target(banner_target)
                self.num_banners_closed += 1
                time.sleep(1)
                self.fix_accidents()

            else:
                skip_ad_target = self.find_img_center(self.skip_img, self.skip_ad_region_pixels)

                if skip_ad_target is not None:
                    self.click_target(skip_ad_target)
                    self.num_video_ads_skipped += 1
                    time.sleep(1)
                    self.fix_accidents()

            _, mouse_y = pag.position()  # Leave the loop when the cursor is at the bottom of the screen

    def find_img_center(self, image_file, region):
        search_result = pag.locateOnScreen(image=image_file, grayscale=True, region=region,
                                           confidence=self.searching_confidence)

        if search_result is not None:
            return pag.center(search_result)
        else:
            return None

    def click_target(self, target_to_click, x_offset=0, y_offset=0):
        original_mouse_position = pag.position()
        click_x = target_to_click.x
        click_x += x_offset
        click_y = target_to_click.y
        click_y += y_offset
        pag.click(click_x, click_y)
        pag.moveTo(original_mouse_position[0], original_mouse_position[1], self.movement_delay_s)

    def fix_accidents(self):
        search_result = self.find_img_center(self.play_img, self.pause_region_pixels)
        if search_result is not None:
            self.click_target(search_result)

    @staticmethod
    def region_rel_to_abs(rel_array, width, height):
        value_left = int(width * rel_array[0])
        value_top = int(height * rel_array[1])
        value_width = int(width * rel_array[2])
        value_height = int(height * rel_array[3])
        return value_left, value_top, value_width, value_height
