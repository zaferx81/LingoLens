import argostranslate.package

TARGET_PACKAGES = [
    ("en", "de"),
    ("en", "fr"),
    ("en", "es"),
    ("en", "ru"),
    ("en", "zh"),
]

print("Paket listesi güncelleniyor...")
argostranslate.package.update_package_index()

available_packages = argostranslate.package.get_available_packages()

for from_code, to_code in TARGET_PACKAGES:
    print(f"\nAranıyor: {from_code} → {to_code}")

    package = next(
        (
            pkg for pkg in available_packages
            if pkg.from_code == from_code and pkg.to_code == to_code
        ),
        None
    )

    if package is None:
        print(f"Bulunamadı: {from_code} → {to_code}")
        continue

    print(f"İndiriliyor: {from_code} → {to_code}")
    download_path = package.download()

    print(f"Kuruluyor: {from_code} → {to_code}")
    argostranslate.package.install_from_path(download_path)

    print(f"Tamamlandı: {from_code} → {to_code}")

print("\nTüm uygun paketler tamamlandı.")