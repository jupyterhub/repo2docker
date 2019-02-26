#!/bin/julia

# Path to potential REQUIRE file is passed on the command line.
require_file = ARGS[1]

if VERSION < v"0.7-"
  pkg_dir = "$(ENV["JULIA_PKGDIR"])/v$(VERSION.major).$(VERSION.minor)"
  open("$pkg_dir/REQUIRE", "a") do io
    write(io, read(require_file))
  end
  Pkg.resolve();
  Reqs = Pkg.Reqs
else
  using Pkg
  Reqs = Pkg.Pkg2.Reqs
  emptyversionlower = v"0.0.0-"
  for reqline in Reqs.read(require_file)
    if reqline isa Reqs.Requirement
        pkg = String(reqline.package)
        if pkg == "julia" continue end
        version = try; reqline.versions.intervals[1].lower; catch; emptyversionlower; end
        if version != emptyversionlower
          Pkg.add(PackageSpec(name=pkg, version=version))
        else
          Pkg.add(pkg)
        end
    end
  end
end
# Precompile the packages
for reqline in Reqs.read(require_file)
  if reqline isa Reqs.Requirement
      pkg = reqline.package
      pkg != "julia" && eval(:(using $(Symbol(pkg))))
  end
end
