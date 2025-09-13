#!/usr/bin/env python3
import qrcode, argparse
p = argparse.ArgumentParser()
p.add_argument("--input", required=True)
p.add_argument("--output", required=True)
args = p.parse_args()
qr = qrcode.QRCode(version=1, box_size=10, border=4)
qr.add_data(f"SHA-713 Proof :: {args.input}")
qr.make(fit=True)
qr.make_image(fill_color="black", back_color="white").save(args.output)
print("QR generado:", args.output)

