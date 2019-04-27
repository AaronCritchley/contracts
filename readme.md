[![Build Status](https://travis-ci.org/bluecoveltd/contracts.svg?branch=master)](https://travis-ci.org/bluecoveltd/contracts)
[![codecov](https://codecov.io/gh/bluecoveltd/contracts/branch/master/graph/badge.svg)](https://codecov.io/gh/bluecoveltd/contracts)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/b7e92327c90e4fa895d9dc53224053b2)](https://www.codacy.com/app/AaronCritchley/contracts?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=bluecoveltd/contracts&amp;utm_campaign=Badge_Grade)

# BlueCove Contracts

This is a hard fork of the PyContracts library, the original version
of which can be found [here](https://github.com/AndreaCensi/contracts).

Modifications we have made:

- All contract definitions are now applied at all times. Previously
  if you added type annotations to a function, the docstring contracts
  were ignored. Type annotations and docstring contracts have different
  (but overlapping) purposes, and therefore we require both.
  Also, previously if you used a contract decorator then both type
  annotations and docstring contracts were ignored. This is also fixed.
- Removed Python 2.x support. Maintaining support for legacy python
  versions bloats the codebase significantly, so we only support Python
  3.5+.
  
### Why did we fork?

We are big fans of the original project from Andrea Censi, and we are
very happy to merge these changes upstream, however we received
no response from the original project, and therefore we assume the 
project is orphaned.

There are also wider changes we want to make across the codebase, so we
also crossed the threshold where it became viable to maintain our own
codebase.