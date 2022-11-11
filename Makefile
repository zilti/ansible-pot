##
# Ansible Pot Role
#
# @file
# @version 0.1

README.org: pot.org
	emacs pot.org --batch --kill --eval '(setq org-confirm-babel-evaluate nil)' -f org-org-export-to-org
	mv pot.org.org README.org
	git add README.org

# end
