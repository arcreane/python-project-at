import pygame
import random

class CodeMiniGame:
    def __init__(self):
        self.active = False
        self.secret_word = ""
        self.tries = 0
        self.max_tries = 5
        self.start_time = None
        self.time_limit = 180
        self.font = pygame.font.SysFont("couriernew", 24)
        self.title_font = pygame.font.SysFont("couriernew", 28)
        self.result = None
        self.selected_index = 0
        self.words = ["ROCKET", "TARGET", "MARKET", "POCKET", "LOCKET", "BUCKET", "RACKET", "SOCKET"]
        self.traps = ["##$%^&", "*(&^%$", "]]]]]]"]
        self.left_column = []
        self.right_column = []
        self.feedback = ""
        self.secret_door_unlocked = False
        self.mail_access = False
        self.mail_entries = ["- SECURITY REPORT", "- MEDICAL LOG", "- UNKNOWN FILE", "- OPEN VAULT"]
        self.mail_selected = 0
        pygame.mixer.init()
        self.error_sound = pygame.mixer.Sound("../Audio/error.mp3")
        self.success_sound = pygame.mixer.Sound("../Audio/success.mp3")

    def start(self):
        self.active = True
        self.tries = 0
        self.start_time = pygame.time.get_ticks()
        self.result = None
        self.selected_index = 0
        self.secret_word = random.choice(self.words)
        random.shuffle(self.words)
        combined = []
        trap_index = 0
        for i, word in enumerate(self.words):
            combined.append(word)
            if i % 2 == 1:
                combined.append(self.traps[trap_index % len(self.traps)])
                trap_index += 1
        if len(combined) % 2 != 0:
            combined.append(random.choice(self.traps))
        half = len(combined) // 2
        self.left_column = combined[:half]
        self.right_column = combined[half:]
        self.feedback = ""
        self.secret_door_unlocked = False
        self.mail_access = False
        self.mail_selected = 0

    def handle_event(self, event):
        if not self.active:
            return

        if not self.mail_access:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if self.selected_index > 0:
                        self.selected_index -= 1
                elif event.key == pygame.K_DOWN:
                    if self.selected_index < len(self.left_column + self.right_column) - 1:
                        self.selected_index += 1
                elif event.key == pygame.K_LEFT:
                    if self.selected_index >= len(self.left_column):
                        self.selected_index -= len(self.left_column)
                elif event.key == pygame.K_RIGHT:
                    if self.selected_index < len(self.left_column):
                        self.selected_index += len(self.left_column)
                elif event.key == pygame.K_RETURN:
                    selected = (self.left_column + self.right_column)[self.selected_index]
                    if selected in self.words:
                        if selected == self.secret_word:
                            self.result = "win"
                            self.feedback = "ACCESS GRANTED\nENTERING MESSAGE SYSTEM..."
                            self.success_sound.play()
                            self.secret_door_unlocked = False
                            self.mail_access = True
                        else:
                            correct = sum(a == b for a, b in zip(selected, self.secret_word))
                            self.feedback = f"{correct}/{len(self.secret_word)} CORRECT"
                            self.tries += 1
                            self.error_sound.play()
                            if self.tries >= self.max_tries:
                                self.result = "lose"
                                self.active = False
                                self.feedback = "ACCESS DENIED"
                    else:
                        self.feedback = "TRAP ACTIVATED! TRY LOST"
                        self.tries += 1
                        self.error_sound.play()
                        if self.tries >= self.max_tries:
                            self.result = "lose"
                            self.active = False
                            self.feedback = "ACCESS DENIED"
        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.active = False
                elif event.key == pygame.K_UP:
                    if self.mail_selected > 0:
                        self.mail_selected -= 1
                elif event.key == pygame.K_DOWN:
                    if self.mail_selected < len(self.mail_entries) - 1:
                        self.mail_selected += 1
                elif event.key == pygame.K_RETURN:
                    selected_entry = self.mail_entries[self.mail_selected]
                    if selected_entry == "- OPEN VAULT":
                        self.feedback = "MESSAGE: VAULT DOOR UNLOCKED"
                        self.secret_door_unlocked = True
                    elif selected_entry == "- SECURITY REPORT":
                        self.feedback = "SECURITY REPORT:\nEffectif réduit. Aucun remplaçant disponible."
                    elif selected_entry == "- MEDICAL LOG":
                        self.feedback = "MEDICAL LOG:\nLes patients montrent une agressivité accrue."
                    elif selected_entry == "- UNKNOWN FILE":
                        self.feedback = "??: \u2593\u2591\u2593\u2588\u2592\u2592\u2592 ERROR\u2588\u2593\u2591"

    def update(self):
        if not self.active:
            return
        elapsed = (pygame.time.get_ticks() - self.start_time) / 1000
        if elapsed > self.time_limit and not self.mail_access:
            self.result = "timeout"
            self.active = False
            self.feedback = "ACCESS DENIED"

    def render(self, screen):
        if not self.active:
            return

        screen.fill((0, 0, 0))
        green = (0, 255, 0)
        line_height = self.font.get_linesize()

        screen.blit(self.title_font.render("ROBCO URSS (TM) TERMLINK PROTOCOL", True, green), (50, 20))

        if not self.mail_access:
            screen.blit(self.font.render("ENTER PASSWORD NOW", True, green), (50, 60))
            screen.blit(self.font.render(f"{self.max_tries - self.tries} ATTEMPT(S) LEFT", True, green), (50, 100))

            for i, entry in enumerate(self.left_column):
                x, y = 50, 140 + i * line_height
                is_selected = self.selected_index == i
                color = (0, 0, 0) if is_selected else green
                bg = green if is_selected else None
                screen.blit(self.font.render(f"0x{1000 + i*10:04X} {entry}", True, color, bg), (x, y))

            for j, entry in enumerate(self.right_column):
                x, y = 400, 140 + j * line_height
                idx = len(self.left_column) + j
                is_selected = self.selected_index == idx
                color = (0, 0, 0) if is_selected else green
                bg = green if is_selected else None
                screen.blit(self.font.render(f"0x{1040 + j*10:04X} {entry}", True, color, bg), (x, y))

        else:
            screen.blit(self.font.render("INBOX MESSAGES:", True, green), (50, 80))
            for i, msg in enumerate(self.mail_entries):
                color = (0, 0, 0) if i == self.mail_selected else green
                bg = green if i == self.mail_selected else None
                screen.blit(self.font.render(msg, True, color, bg), (80, 120 + i * line_height))

        if self.feedback:
            lines = self.feedback.split("\n")
            for i, line in enumerate(lines):
                screen.blit(self.font.render(line, True, green), (50, 520 + i * line_height))
