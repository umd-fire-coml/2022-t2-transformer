if [ -f "song-clip-triplets.zip" ]; then
    echo "Dataset already downloaded."
else
    echo "Downloading dataset..."
    kaggle datasets download -d rishipradeep/song-clip-triplets
fi

if [ -d "triplets" ]; then
    echo "Dataset already unzipped."
else
    echo "Unzipping dataset..."
    unzip ./song-clip-triplets.zip
fi
