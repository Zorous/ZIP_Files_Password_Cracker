import zipfile
import itertools
import string
import multiprocessing

def try_password(zip_file, password):
    """Try to open the ZIP file with the given password."""
    try:
        with zipfile.ZipFile(zip_file) as zf:
            zf.setpassword(password.encode())
            zf.testzip()  # Check if password works
            return True
    except RuntimeError:
        return False

def brute_force_chunk(zip_file, charset, start, end, length):
    """Process a chunk of password combinations and return the correct one if found."""
    count = 0
    for password_tuple in itertools.product(charset, repeat=length):
        if count >= start and count < end:
            password = ''.join(password_tuple)
            print(f"Trying password: {password}")
            if try_password(zip_file, password):
                return password
        count += 1
    return None

def split_work(total_combinations, num_chunks):
    """Split the total number of combinations into chunks."""
    chunk_size = total_combinations // num_chunks
    ranges = [(i * chunk_size, (i + 1) * chunk_size) for i in range(num_chunks)]
    return ranges

def brute_force_zip(zip_file, charset, min_length, max_length, num_workers=4):
    """Parallel brute-force ZIP file password recovery."""
    for length in range(min_length, max_length + 1):
        total_combinations = len(charset) ** length  # Total number of possible combinations for this length
        ranges = split_work(total_combinations, num_workers)

        # Create a pool of workers
        with multiprocessing.Pool(processes=num_workers) as pool:
            results = pool.starmap(brute_force_chunk, [(zip_file, charset, start, end, length) for start, end in ranges])

        # Check results and return the found password
        for result in results:
            if result:
                print(f"Password found: {result}")
                return result
    return None

if name == 'main':
    # Example usage
    zip_file = r'C:\your\file\path\file.zip'  # Replace with your ZIP file path
    charset = string.ascii_lowercase + string.ascii_uppercase + string.digits  # Character set for password
    min_length = 1  # Min password length to try
    max_length = 10  # Max password length to try
    num_workers = 4  # Number of parallel processes (threads ) i set it to 4 for safety  (adjust based on your CPU)

    password = brute_force_zip(zip_file, charset, min_length, max_length, num_workers)
    if password:
        print(f"Password found: {password}")
    else:
        print("Password not found.")