#include "cli.h"

int main(void) {
  InitNcurses();
  int key = getch();
  while (key != 27) {
    erase();
    ShowMainMenu();
    if (key == 't' || key == 'T') {
      clear();
      GameLoop(1);
    } else if (key == 's' || key == 'S') {
      clear();
      GameLoop(2);
    } else if (key == 'r' || key == 'R') {
      clear();
      system("python3 brick_game/race/race_c.py");
    }
    key = getch();
  }
  EndNcurses();
  return 0;
}
