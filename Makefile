##
# Ansible Pot Role
#
# @file
# @version 0.1

README.org zilti/pot/README.org zilti/pot/README.md: pot.org
	mkdir -p zilti/pot
	emacs pot.org --batch --kill \
	--eval '(setq org-confirm-babel-evaluate nil)' \
	-f org-org-export-to-org \
	-f org-md-export-to-markdown
	mv pot.org.org README.org
	cp README.org zilti/pot/README.org
	git add README.org
	git add zilti/pot/README.org

# end
