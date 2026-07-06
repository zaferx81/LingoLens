import argostranslate.package
import argostranslate.translate

from_code = "en"
to_code = "tr"

print("Model listesi güncelleniyor...")
argostranslate.package.update_package_index()

available_packages = argostranslate.package.get_available_packages()

package_to_install = next(
    filter(
        lambda x: x.from_code == from_code and x.to_code == to_code,
        available_packages
    ),
    None
)

if package_to_install is None:
    print("English -> Turkish modeli bulunamadı.")
else:
    print("Model indiriliyor ve kuruluyor...")
    argostranslate.package.install_from_path(package_to_install.download())
    print("Model kuruldu: English -> Turkish")

input("\nÇıkmak için Enter...")
