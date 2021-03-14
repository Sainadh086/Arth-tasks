import os
import subprocess

print("\t\t\tWelcome to use LVM")
print("\t\tHere you can add extra volume, resize and reduce")
print("\t\tHere we are now supporting only Amazon EC2 as of now and local devices")

ans = input("Using remote devices(y/n)")
vg_name = "my_vg"
lv_name = "my_lv"
if(ans=='y'):
    user = input("Enter the name of your EC2 instance eg:-user@121.03.01.23: ")
    path = input("Enter the path for key file: ")
    ssh = f"ssh -i {path} {user}"
    os.system(f"{ssh} fdisk -l | grep /dev/")
    while(True):
        print("Please select from the below options \nPress 1 for lvm commands installation.\nPress 2 for mounting lvm to a drive. \nPress 3 for increasing the drive or partition size.\nPress 4 for decreasing the drive or partition size. \nPress 5 for exit.")
        f_name = None
        ssh = f"ssh -i {path} {user}"
        scp = f"ssh -i {path} {f_name} {user}:~/"
        choice = int(input())
        if(choice==1):
            os.system(f"{ssh} sudo yum install lvm2 -y")
        elif(choice==2):
            num = int(input("Enter number of partition drives to configure: "))
            drive_names = []
            for i in range(num):
                drive_name = input("Enter the storage path: ")
                drive_names.append(drive_name)
                os.system(f"{ssh} sudo pvcreate {drive_name}")
            os.system(f"{ssh} sudo  pvdisplay") 
            disk_names = " ".join(drive_names)
            os.system(f"{ssh} sudo vgcreate {vg_name} {disk_names}")
            os.system(f"{ssh} sudo vgdisplay {vg_name}")
            size = int(input("Enter the size in GB for LVM"))
            print("Creating lvm")
            os.system(f"{ssh} sudo lvcreate --size {size}G --name {lv_name} {vg_name}")
            os.system(f"{ssh} sudo lvdisplay")
            folder_name = input("Enter folder name to mount the lvm partition: ")
            os.system(f"{ssh} sudo mkdir /{folder_name}")
            os.system(f"{ssh} sudo mkfs.ext4 /dev/{vg_name}/{lv_name}")
            os.system(f"{ssh} sudo mount /dev/{vg_name}/{lv_name} /{folder_name}")
            os.system(f"{ssh} sudo df -h | grep /dev/")
            print("Succesfully created LVM\n")
            print(f"vg name: {vg_name} \nlvm name: {lv_name} \nsize: {size}")
        elif(choice == 3):
            size = input("Enter the expected size of drive to be increased: ")
            os.system(f"{ssh} sudo lvextend --size {size}G /dev/{vg_name}/{lv_name}")
            os.system(f"{ssh} sudo resize2fs /dev/{vg_name}/{lv_name}")
            os.system(f"{ssh} sudo df -h | grep /dev/")
            print("Drive size incresed successfully")
        elif(choice == 4):
            or_size = int(input("Enter the original drive size: "))
            re_size = int(input("Enter the drive size to reduce: "))
            new_size = or_size-re_size
            if(new_size>0):
                print("Note:- While  reducing you will lose the data \nPress y to stop")
                ans_dec = input()
                if(ans_dec == 'y'):
                    break
                os.system(f"{ssh} sudo umount /dev/{vg_name}/{lv_name}")
                os.system(f"{ssh} sudo e2fsck -f /dev/{vg_name}/{lv_name}")
                os.system(f"{ssh} sudo resize2fs /dev/{vg_name}/{lv_name} {new_size}")
                os.system(f"{ssh} sudo lvreduce -L -{re_size}G /dev/{vg_name}/{lv_name}")
                os.system(f"{ssh} sudo mkfs.ext4 /dev/mapper/my_vg-my_lv")
                folder_name = input("Enter the folder name to mount: ")
                os.system(f"{ssh} sudo mkdir /{folder_name}")
                os.system(f"{ssh} sudo mount /dev/{vg_name}/{lv_name} /{folder_name}")
                os.system(f"{ssh} sudo df -h | grep /dev/")
                print("Drive is succesfully resized")
            else:
                print("Drive size to reduce is larger than the original size.\nCannot proceed to resize")
        elif(choice == 5):
            break
        else:
            print("Press the right option from below")
    else:
        print("please follow the below steps")
        fd = open("lvm.txt", "r")
        print(fd.read())
        fd.close()
