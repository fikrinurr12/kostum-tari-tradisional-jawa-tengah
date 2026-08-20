"""
utils/selfie_detector.py  —  TariJateng
Deteksi selfie sebagai LAPIS 0, dijalankan sebelum inferensi model
klasifikasi kostum tari (hemat compute, selfie langsung ditolak tanpa
perlu memanggil CNN).

Metode: Haar Cascade frontal face (OpenCV) untuk mendeteksi wajah, lalu
gambar ditandai sebagai selfie jika wajah terbesar mendominasi frame
(rasio luas wajah / luas gambar >= SELFIE_FACE_AREA_THRESHOLD). Foto
kostum tari umumnya berupa shot penuh/menengah badan sehingga wajah
(kalau terdeteksi sekalipun) hanya mengisi sebagian kecil frame — beda
dengan selfie yang biasanya close-up wajah.
"""

import numpy as np
from PIL import Image

import config

_face_cascade = None


def _get_cascade():
    """Lazy-load Haar Cascade agar cv2 hanya di-import saat dibutuhkan."""
    global _face_cascade
    if _face_cascade is None:
        import cv2
        path = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        _face_cascade = cv2.CascadeClassifier(path)
    return _face_cascade


def is_selfie(image: Image.Image) -> dict:
    """
    Mendeteksi apakah gambar kemungkinan besar adalah selfie/foto wajah
    close-up, bukan foto kostum tari.

    Returns:
        dict dengan kunci:
          is_selfie      : bool  — True jika terdeteksi sebagai selfie
          num_faces      : int   — jumlah wajah terdeteksi
          largest_ratio  : float — rasio luas wajah terbesar terhadap
                                    luas gambar (0.0 jika tidak ada wajah)
    """
    import cv2

    cascade = _get_cascade()

    arr = np.array(image.convert("RGB"))
    gray = cv2.cvtColor(arr, cv2.COLOR_RGB2GRAY)

    faces = cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(60, 60),
    )

    if len(faces) == 0:
        return {"is_selfie": False, "num_faces": 0, "largest_ratio": 0.0}

    img_area = gray.shape[0] * gray.shape[1]
    largest_ratio = max((fw * fh) / img_area for (_, _, fw, fh) in faces)

    return {
        "is_selfie": largest_ratio >= config.SELFIE_FACE_AREA_THRESHOLD,
        "num_faces": len(faces),
        "largest_ratio": largest_ratio,
    }
