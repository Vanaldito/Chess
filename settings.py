class Settings:
    """ A class to manage the game settings """

    def __init__(self):
        """ Create a new settings instance """
        self.screen_width = 600
        self.screen_height = 600
        self.screen_size = (self.screen_width, self.screen_height)

        self.dark_color = (0,0,0)
        self.light_color = (255,255,255)