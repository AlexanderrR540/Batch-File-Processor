import asyncio
import aiofiles
import os


async def get_all_txt(folder_path):
    files = os.listdir(folder_path)
    txt_files = []
    
    for file in files:
        file_path = os.path.join(folder_path, file)
        if os.path.splitext(file)[-1].lower() == ".txt" and os.path.getsize(file_path) >= 1:
            txt_files.append(file_path)

    return txt_files


async def txt_processing(file):
    async with aiofiles.open(file, "r", encoding="utf-8") as f:
        text = await f.read()
    
    symbols1 = [".", "?", "!"]
    symbols2 = [";", ":", ","]

    text = " ".join(text.split())
    letters = list(text)

    up_letter = True
    for i in range(len(letters)):
        if letters[i] in symbols1:
            up_letter = True
            if i != len(letters) - 1:
                if letters[i + 1] != " ":
                    letters[i] = f"{letters[i]} "
        elif letters[i] in symbols2:
            if i != len(letters) - 1:
                if letters[i + 1] != " ":
                    letters[i] = f"{letters[i]} "
        else:
            if up_letter and letters[i] != " ":
                letters[i] = letters[i].upper()
                up_letter = False
            else:
                letters[i] = letters[i].lower()

    async with aiofiles.open(file, "w", encoding="utf-8") as f:
        print(f"{file} changed!")
        await f.write("".join(letters))


async def files_processing(files):
    tasks = []

    for file in files:
        task = asyncio.create_task((txt_processing(file)))
        tasks.append(task)

    await asyncio.gather(*tasks)

async def main():
    folder_path = input("Enter the path to the folder whose files you want to process:\n")

    files = await get_all_txt(folder_path)
    await files_processing(files)

    print("Done!")
    

if __name__ == '__main__':
    asyncio.run(main())