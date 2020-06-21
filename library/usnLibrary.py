import apt

def checkPackage(package):
  aptCache = apt.cache.Cache()
  for p in aptCache:
    if p.is_installed:
      if p.name == package:
        if p.versions[0].version > p.installed.version:
          return package
          break
