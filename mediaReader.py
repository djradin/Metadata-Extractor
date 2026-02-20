from pymediainfo import MediaInfo


def get_media_data(path):
    media_data = MediaInfo.parse(path)

    for track in media_data.tracks:
        if track.track_type == "Video":
            print("\nVIDEO DATA")
            print("Bit rate:", track.bit_rate)
            print("Frame rate:", track.frame_rate)
            print("Format:", track.format)
            print("Duration:", track.other_duration[1])

        elif track.track_type == "Audio":
            print("\nAUDIO DATA")
            audio_data = track.to_data()

            for key, value in audio_data.items():
                if "other" in key.lower() or "kind" in key.lower():
                    continue

                if "duration" in key.lower():
                    value = f"{value}ms"

                print(f"{key}: {value}")