##
# Ansible Pot Role
#
# @file
# @version 0.1

zilti/pot/README.org: pot.org
	mkdir -p zilti/pot
	emacs pot.org --batch --kill --eval '(setq org-confirm-babel-evaluate nil)' -f org-org-export-to-org
	mv pot.org.org zilti/pot/README.org
	git add zilti/pot/README.org

# end
