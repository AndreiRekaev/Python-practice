#include "mainwindow.h"

#include <QDir>
#include <QProcess>

#include "ui_mainwindow.h"

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent), ui(new Ui::MainWindow), currentGame(nullptr) {
  ui->setupUi(this);
}

MainWindow::~MainWindow() { delete currentGame; }

void MainWindow::on_tetrisButton_clicked() {
  // Код для запуска Tetris
  GameWidget game = GameWidget(nullptr, 1);
  game.setModal(true);
  game.exec();
}

void MainWindow::on_snakeButton_clicked() {
  // Код для запуска Snake
  GameWidget game = GameWidget(nullptr, 2);
  game.setModal(true);
  game.exec();
}

void MainWindow::on_raceButton_clicked() {
  QProcess *process = new QProcess(this);
  QString pythonExecutable =
      "python3"; // или "python3", в зависимости от вашей системы

  // Получение пути к текущему исполняемому файлу и построение относительного
  // пути
  QString currentDir = QDir::currentPath();
  QString scriptPath = currentDir + "/gui/desktop/gamewindow.py";

  process->setStandardOutputFile("output.log");
  process->setStandardErrorFile("error.log");

  process->start(pythonExecutable, QStringList() << scriptPath);

  // Проверка на успешный запуск
  if (!process->waitForStarted()) {
    qDebug() << "Failed to start process";
    qDebug() << process->errorString();
  } else {
    qDebug() << "Process started successfully";
  }
}
