#!/usr/bin/env python

TOP = '.'
APPNAME = 'WCP'

# the sequence matters
subdirs = [
           'nanoflann',
           'quickhull',
           'data',
           'ress',
           'nav',
           'signal',
           'sst',
           'tiling',
           'rootvis',
           'graph',
           'examples',
           'matrix',
           '2dtoy',
           'lsp',
           'paal',
           'pid',
           'mcs',
           '3dst',
           'uboone_sp_app',
           'uboone_light_app',
           'uboone_nusel_app',
           'uboone_eval_app',
           'uboone_bdt_app',
           'icarus_app',
           'dune_app',
           'pyutil',
           'pyinf'
]

def options(opt):
    opt.load('doxygen', tooldir='waf-tools')
    opt.load('find_package', tooldir='waf-tools')
    opt.add_option('--build-debug', default='-O2',
                   help="Build with debug symbols")
    opt.add_option('--doxygen-tarball', default=None,
                   help="Build Doxygen documentation to a tarball")

def configure(cfg):
    cfg.env.append_unique('CXXFLAGS',['--std=c++14'])
    cfg.load( "compiler_cxx" )

    cfg.load('doxygen', tooldir='waf-tools')
    cfg.load('find_package', tooldir='waf-tools')
    cfg.env.CXXFLAGS += [cfg.options.build_debug, "-Wno-deprecated-declarations"]
    cfg.check_boost(lib='system filesystem graph')

def build(bld):
    bld.load('find_package', tooldir='waf-tools')
    for pkg,ext in dict(paal="GLPK_H", pid="GLPK_H").items():
        have='HAVE_'+ext
        if have in bld.env:
            continue
        if pkg in subdirs:
            print ('Removing package "%s" due to lack of "%s"'%(pkg,ext))
            subdirs.remove(pkg)
    bld.recurse(subdirs)
    if bld.env.DOXYGEN and bld.options.doxygen_tarball:
        bld(features="doxygen", doxyfile=bld.path.find_resource('Doxyfile'),
            doxy_tar = bld.options.doxygen_tarball)

