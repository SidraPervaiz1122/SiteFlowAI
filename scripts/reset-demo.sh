#!/bin/bash
set -e
echo "Resetting SiteFlow AI Demo Database..."
python -m backend.db.seed
echo "SiteFlow AI database reset complete. Exact 24 BOQ items ready."
