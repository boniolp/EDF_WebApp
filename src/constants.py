deb1 = ["DEB1-1", "DEB1-2", "DEB1-3", "DEB1-4"]  # Débit de fuite au joint 1 (Gamme Large)
deb2 = ["DEB2-1", "DEB2-2", "DEB2-3", "DEB2-4"]  # Débit de fuite au joint 1 (Gamme Étroite)
deb3 = ["DEB3-1", "DEB3-2", "DEB3-3", "DEB3-4"]  # Débit d'injection au joint
tmp = ["TEM3-1", "TEM3-2", "TEM3-3", "TEM3-4"]  # Température eau joint 1 - 051PO ### A rapprocher de DEB1 DEB2
tmp2 = ["TEM1-", "TEM2-"]  # Température ligne d'injection aux joints (en * Celsius) / Température fuite joint 1
deb35 = ["DEB3-5"]  # Débit d'injection au joint
vit = ["VIT-1", "VIT-2", "VIT-3", "VIT-4"]  # Vitesse de rotation
pre = ["PRE-"]
pui = ["PUI-"]
MAX_VALUE = 32767.0
THRESHOLD = 1000
MAX_GRANULARITY = 10 # max granularity in minutes

TREND_UP = "t_u"
TREND_DOWN = "t_d"
OSCILLATION = "osc"
STEP = "step"
SPIKE = "spike"