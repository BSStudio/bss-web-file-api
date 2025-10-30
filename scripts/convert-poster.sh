#!/usr/bin/env sh
if [[ "$#" -ne 2 ]]; then
    echo "1st argument: input image"
    echo "2nd argument: output folder"
    exit
fi

mkdir -p $2
magick $1 -quality 60 -resize 1920x1080 -define heic:speed=0 $2/1080.avif
magick $1 -quality 75 -resize 1920x1080                      $2/1080.webp
magick $1 -quality 75 -resize 1920x1080                      $2/1080.jpeg
magick $1 -quality 60 -resize 240 -define heic:speed=0 $2/720.avif
magick $1 -quality 75 -resize 240                      $2/720.webp
magick $1 -quality 75 -resize 240                      $2/720.jpeg
magick $1 -quality 60 -resize 480 -define heic:speed=0 $2/lg.avif
magick $1 -quality 75 -resize 480                      $2/lg.webp
magick $1 -quality 75 -resize 480                      $2/lg.jpeg
magick $1 -quality 60 -resize 960 -define heic:speed=0 $2/xl.avif
magick $1 -quality 75 -resize 960                      $2/xl.webp
magick $1 -quality 75 -resize 960                      $2/xl.jpeg

ls -la $2
