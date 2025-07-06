#!/bin/bash

PYTHON_EXECUTABLE="python3"

pkg install rust
pkg install binutils

install_package() {
  package="$1"
  echo "Установка пакета: $package"
  "$PYTHON_EXECUTABLE" -m pip install "$package"
  if [ $? -eq 0 ]; then
    echo "Пакет $package успешно установлен."
  else
    echo "Ошибка при установке пакета $package."
    exit 1
  fi
}

packages=(
  "kurigram"
  "pyyaml"
  "colorama"
  "tgcrypto"
  "aiohttp"
  "fastapi"
  "uvicorn"
)

# Устанавливаем пакеты
for package in "${packages[@]}"; do
  install_package "$package"
done

echo "Все пакеты успешно установлены."

REPO_URL="http://f1144757.xsph.ru/YuMino_1.3.zip"
REPO_NAME="YuMino_1.3.zip"
EXTRACTED_DIR="YuMino"

if [ -d "$EXTRACTED_DIR" ]; then
  echo "$EXTRACTED_DIR уже существует."
  mv "$EXTRACTED_DIR" "${EXTRACTED_DIR}_$(date +%Y%m%d%H%M%S).bak"
fi

if ! command -v unzip &> /dev/null
then
  echo "unzip не найден. Установка unzip..."
  pkg install unzip
  echo"unzip был установлен. скрипт завершён"
  exit 1
fi

echo "Установка юзербота..."
wget "$REPO_URL" -O "$REPO_NAME"
if [ $? -ne 0 ]; then
  echo "Ошибка при установки юзербота."
  exit 1
fi
echo "юзербот скачан"

echo "Распаковка репозитория..."
unzip "$REPO_NAME" -d "$EXTRACTED_DIR"

if [ $? -ne 0 ]; then
    echo "Ошибка при распаковке юзербота.  Убедитесь, что установлен unzip."
    rm "$REPO_NAME"
    exit 1
fi
echo "Юзербот распакован в папку $EXTRACTED_DIR"

rm "$REPO_NAME"

if [ ! -d "$EXTRACTED_DIR" ]; then
    echo "Внимание: $EXTRACTED_DIR не найден. Убедитесь, что он существует."
    exit 1
fi

echo "Переход в $EXTRACTED_DIR"
cd "$EXTRACTED_DIR"

"$PYTHON_EXECUTABLE" main.py

echo "Скрипт завершен."
exit 0
