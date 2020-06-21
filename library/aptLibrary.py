import apt

def checkPackageIsInstalled(package):
  aptCache = apt.cache.Cache()
  for p in aptCache:
    if p.is_installed:
      if p.name == package:
        return package
        break

def checkPackageUpgrade(package):
  aptCache = apt.cache.Cache()
  for p in aptCache:
    if p.is_installed:
      if p.name == package:
        if p.versions[0].version > p.installed.version:
          return package
          break

def checkPackageVersion(package, version):
  aptCache = apt.cache.Cache()
  for p in aptCache:
    if p.is_installed:
      if p.name == package:
        print(p.installed.version)
        print(version)
        if p.installed.version < version:
          return package
          break
