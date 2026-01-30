# Path to the log directory
LOGDIR="$HOME/Downloads/LibreOffice_Log"

# Path to the log file
LOGFILE="$LOGDIR/LibreOffice_Log.txt"

# Create the log directory if it does not exist
mkdir -p "$LOGDIR"

# Process each file passed from Automator
for f in "$@"
do
    echo "-----" >> "$LOGFILE"
    echo "Start converting: $f" >> "$LOGFILE"
    echo "Time: $(date)" >> "$LOGFILE"

    # Folder where the original file is located
    dir=$(dirname "$f")

    # Run LibreOffice in headless mode
    /Applications/LibreOffice.app/Contents/MacOS/soffice \
        --headless --convert-to pdf --outdir "$dir" "$f" \
        >> "$LOGFILE" 2>&1

    # Check exit status
    if [ $? -eq 0 ]; then
        echo "Success: PDF saved to $dir" >> "$LOGFILE"
        open "$dir"      # On success: open the PDF folder
    else
        echo "ERROR: Conversion failed for $f" >> "$LOGFILE"
        open "$LOGDIR"   # On failure: open the log folder
    fi

    echo "" >> "$LOGFILE"
done