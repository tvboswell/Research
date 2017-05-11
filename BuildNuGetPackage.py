############################################################################################################################
# BuildNuGetPackage.py - Builds and publishes a NuGet package for a back-end C# library or application.
#
#   Arg1 = Solution directory
#   Arg2 = Configuration (Debug or Release)
#
############################################################################################################################

# System imports
import os
import sys
import subprocess

# Add path to %PF% folder so we can find other scripts.
sys.path.insert(0, os.environ['PF'])

# Proprietary imports
from PackageJson import PackageJson
from ProtoGen import ProtoGen
from Solution import Solution
from Project import Project
from NuGet import NuGet
from Process import Process
from Exceptions import BuildException

# See if this is the messages library which requires proto file generation
if "pf-messages-library" in sys.argv[1]:
	pg = ProtoGen()
	pg.Run()

# Initialization
solutionDir = sys.argv[1] 
configuration = sys.argv[2]
packageDir = os.path.abspath(os.path.join(solutionDir))

print("==================== PUBLISHING " + packageDir + " STARTED ====================\n") 

os.chdir(packageDir)

# Read packaging information from package.json file in repository root.
packageJson = PackageJson(packageDir, configuration)

# Find the solution in Source directory (also creates all associated Project objects for Solution)
solution = Solution(solutionDir, packageJson, configuration)

# Synchronize AssemblyInfo.cs versions to what's in package.json file.
for project in solution.Projects: project.SynchronizeVersions()

# Restore any missing NuGet packages for solution before building.
nuget = NuGet(solution, packageJson)
nuget.RestoreMissingPackages()

# Update NuGet packages before building.
nuget.UpdatePackages()

# Build the solution.
solution.Build()

# Publish the package to local registry.
nuget.PublishToLocalRegistry()

print("\n==================== PUBLISHING " + packageDir + " COMPLETED ====================")
