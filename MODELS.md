Model Architecture Planning

Membership
	-slug
	-type (free, pro, enterprise)
	-price
	-stripe id

userMembership
	- user  (foreigney to user)
	-stripe customer id 	(created automatically)
	-membership type  (foreignkey to membership)

Subscription
	- user membership    (foreignkey to Usermembership)
	- stripe subscription id  
	- active


Course
	- slug
	- title
	- description
	- allowed membership 	(manytomany to membership)

Lesson
	- slug
	- title
	- course				(foreignkey to course)
	- position
	- video
	- thumbnail



