# OCR4ZN-Hospital
OCR scripts for WSI rename of ZN-Hospital 

## Envs
`conda create -n ZN-OCR python=3.9`

`pip install paddleocr,paddlepaddle,pandas,sdpc-for-python`
## Settings
`Use Sdpc.py to replace the Sdpc.py in XXX/Anaconda3/envs/ZN-OCR/Lib/site-packages/sdpc/Sdpc.py`

## Run the script
`conda activate ZN-OCR`

`set Params (WSI_DIR_LIST and WORK_DIR) in ZN-Hospital-WSIs-Rename.py`

`python ZN-Hospital-WSIs-Rename.py`

## Description
`Due to handwriting and recognition accuracy issues, manual subsequent modifications are required`
