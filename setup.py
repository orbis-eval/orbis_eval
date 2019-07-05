import os

try:
    from orbis.core.orbis_setup import OrbisSetupBaseClass
    OrbisSetupBaseClass().run(os.path.dirname(os.path.realpath(__file__)))
except Exception as exception:
    print("Orbis not found. Please install Orbis first.")
    print(f"({exception})")

