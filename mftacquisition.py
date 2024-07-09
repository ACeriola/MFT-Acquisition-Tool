import pytsk3
import sys
import os

class Img_Info(pytsk3.Img_Info):
    def __Init__(self, image_file):
        self.image_file = open(image_file, 'rb')
        super(Img_Info, self).__init__(url='', type=pytsk3.TSK_IMG_TYPE_EXTERNAL)
        
    def close(self):
        self.image_file.close()
       
    def read(self, offset, size):
        self.image_file.seek(offset)
        return self.image_file.read(size)
        
    def get_size(self):
        self.image_file.seek(0, 2)
        return self.image_file.tell()
        
def extract_mft(image_path, output_path):
    img_info = Img_Info(image_path)
    fs_info = pytsk3.FS_Info(img_info)
    
    mft_file = fs_info.open_meta(0x00000000)
    
    with open(output_path, 'wb') as f:
        size = mft_file.info.meta.size
        offset = 0
        while offset < size:
            available_to_read = min(1024 * 1024, size - offset)
            data = mft_file.read_random(offset, available_to_read)
            if not data:
                break
            f.write(data)
            offset += len(data)
            
    print(f"$MFT file extracted to {output_path}")
			
if __name__ == "__main__":
	if len(sys.argv) !=2:
		print(f"Usage: {sys.argv[0]} <image path> ")
		sys.exit(1)
		
image_path = sys.argv[1]
output_path = r'C:\Users\admin\Desktop\New Folder (2)\$MFT'


image_path = r'\\.\C:'
    
extract_mft(image_path, output_path)
    
	