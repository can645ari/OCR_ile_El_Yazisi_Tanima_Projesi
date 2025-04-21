from paddleocr import PaddleOCR

class OCREngine:
    def __init__(self):
        self.ocr = PaddleOCR(use_angle_cls=True, lang='tr')

    def recognize_text(self, image_path):
        raw_result = self.ocr.ocr(image_path, cls=True)
        return self.extract_text_lines(raw_result)

    def extract_text_lines(self, ocr_result):
        lines = []
        for line in ocr_result[0]:
            text = line[1][0]  # sadece metin kısmını alıyoruz
            lines.append(text)
        return lines
