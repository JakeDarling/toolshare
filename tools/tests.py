"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from shed.models import Shed
from user.models import Owner
from tools.models import Tool
from datetime import date

class ToolsTest(TestCase):
	def test_public_tool(self):
		"""
		Tests that a tool is public when added to a public shed.
		"""
		test_user = Owner(email='test@rit.com', fname='derick', lname='yung', address='RIT Inn', date_joined=date.today(), zipcode=11421,)
		test_shed = Shed(name='test_shed', zipcode=11421, address_one='RIT Inn', owner_id=test_user.id, owner_string=Owner.objects.get(pk=test_user.id).fname, private=1 )
		test_tool = Tool(name='test', owner_id=1, owner_string='tester', borrower_id=2, borrower_string='testee', shed_id=1)
		self.assertEqual(Shed.objects.get(pk=1).private, 0)

	def test_private_tool(self):
		"""
		Tests that a tool is private when added to private shed.
		"""
		test_user = Owner(email='test@rit.com', fname='derick', lname='yung', address='RIT Inn', date_joined=date.today(), zipcode=11421,)
		test_shed = Shed(name='test_shed', zipcode=11421, address_one='RIT Inn', owner_id=test_user.id, owner_string=Owner.objects.get(pk=test_user.id).fname, private=1 )
		test_tool = Tool(name='test', owner_id=1, owner_string='tester', borrower_id=2, borrower_string='testee', shed_id=1)
		self.assertEqual(Shed.objects.get(pk=1).private, 1)
