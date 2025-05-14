import os
import shutil

def reorganize_replica_dataset(replica_root):
    """
    Reorganize Replica dataset: move RGB and depth images from 'results' into 'images' and 'depth_images' folders.
    """

    # List all room directories
    rooms = [d for d in os.listdir(replica_root) if os.path.isdir(os.path.join(replica_root, d))]
    print(f"Found rooms: {rooms}")

    for room in rooms:
        room_path = os.path.join(replica_root, room)
        results_path = os.path.join(room_path, "results")
        images_path = os.path.join(room_path, "images")
        depth_images_path = os.path.join(room_path, "depth_images")

        if not os.path.exists(results_path):
            print(f"[Warning] No 'results' folder found in {room}, skipping...")
            continue

        # Create target folders
        os.makedirs(images_path, exist_ok=True)
        os.makedirs(depth_images_path, exist_ok=True)

        # Move every file from results/
        files = os.listdir(results_path)
        for file_name in files:
            src = os.path.join(results_path, file_name)
            if os.path.isfile(src):
                if file_name.startswith("frame") and file_name.endswith(".png"):
                    dst = os.path.join(images_path, file_name)
                    print(f"[Move] {file_name} --> images/")
                    shutil.move(src, dst)
                elif file_name.startswith("depth") and file_name.endswith(".png"):
                    dst = os.path.join(depth_images_path, file_name)
                    print(f"[Move] {file_name} --> depth_images/")
                    shutil.move(src, dst)
                else:
                    print(f"[Skip] Unknown file: {file_name}")

        # After moving, remove the empty 'results' folder
        if not os.listdir(results_path):
            os.rmdir(results_path)
            print(f"[Info] Removed empty 'results' folder in {room}")

        print(f"[Info] Finished restructuring {room}")

if __name__ == "__main__":
    # Change this to your actual Replica folder
    replica_root = "dataset/Replica"
    reorganize_replica_dataset(replica_root)
