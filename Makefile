##
# Ansible Pot Role
#
# @file
# @version 0.1

.PHONY: galaxy-publish

VERSION = 0.5.6
GALAXY_ARTIFACT := zilti-pot-${VERSION}.tar.gz

README.org zilti/pot/README.org zilti/pot/README.md zilti/pot/galaxy.yml: pot.org
	mkdir -p zilti/pot
	emacs pot.org --batch --kill \
	--eval '(setq org-confirm-babel-evaluate nil)' \
	--eval "(require 'ob-tangle)" \
	-f org-org-export-to-org \
	-f org-md-export-to-markdown \
	--eval '(org-babel-tangle-file "pot.org")'
	mv pot.org.org README.org
	mv pot.md zilti/pot/README.md
	git add README.org
	git add zilti/pot/README.md

${GALAXY_ARTIFACT}: zilti/pot/galaxy.yml
	rm -rf ${GALAXY_ARTIFACT}
	ln -sf ../../README.md zilti/pot/roles/pot/README.md
	ansible-galaxy collection build zilti/pot/

test:: ${GALAXY_ARTIFACT}
	ansible-galaxy collection install -fn ${GALAXY_ARTIFACT}
	ansible-playbook -i inventory playbook.yml -vvv

galaxy-api-key = ''
galaxy-publish: ${GALAXY_ARTIFACT} README.org
	ansible-galaxy collection publish --api-key	'${galaxy-api-key}' ${GALAXY_ARTIFACT}
	git add pot.org zilti/pot
# end
