# UNSW-talk
An simple school social websit

Andrew has decided he will make himself rich exploiting COMP[29]041 students' coding skills . Andrew's plan is to have COMP[29]041 students create a social media platform for UNSW students called UNSWtalk Because Andrew is unaware of any other competing social media platforms, he thinks UNSWtalk will become very popular and he will become rich.
He wants UNSWtalk to allow students to post messages, other students to comment on these messges and replies to these comments to be added.

He wants UNSWtalk to allows students to indicate other students are their friends.

Your task is to produce either Python or Perl code which provides the core features of UNSWtalk.

In other words your task is to implement a simple but fully functional social media web site.

But don't panic, the assessment for this assignment (see below) will allow you to obtain a reasonable mark if you successfully complete some basic features.


To assist you tackling the assignment, requirements have been broken into several levels in approximate order of difficulty. You do not have to follow this implementation order but unless you are confident I'd recommend following this order. You will receive marks for whatever features you have working or partially working (regardless of subset & order).
Display Student Information & Posts (Level 0)
The starting-point script you've been given (see below) displays student information in raw form and does not display their image or posts.
Your web site should display student information in nicely formatted HTML with appropriate accompanying text. It should display the student's image if there is one.

Private information such e-mail, password, lat, long and courses should not be displayed.

The student's posts should be displayed in reverse chronological order.

Interface (Level 0)
Your web site must generate nicely formatted convenient-to-use web pages including appropriate navigation facilities and instructions for naive students. Although this is not a graphic design exercise you should produce pages with a common and somewhat distinctive look-and-feel. You may find CSS useful for this.
As part of your personal design you may change the name of the website to something other than UNSWtalk but the primary CGI script has to be UNSWtalk.cgi.

Friend list (Level 1)
When a UNSWtalk page is shown a list of the names of that student's friends should be displayed.
The list should include a thumbnail image of the friend (if they have a profile image).

Clicking on the image and/or name should take you to that UNSWtalk page.

Search for Names (Level 1)
Your web site should provide searching for a student whose name contains a specified substring. Search results should include the matching name and a thumbnail image. Clicking on the image and/or name should take you to that UNSWtalk page.
Logging In & Out (Level 1)
Students should have to login to use UNSWtalk.
Their password should be checked when they attempt to log in.

Students should also be able to logout.

Displaying Posts (Level 2)
When a student logs in they should see their recent posts, any posts from their friends and any posts which contain their zid in the post, comments or replies.
Comments and replies should be shown appropriately with posts.

When displaying posts zids should be replaced with a link to the student's UNSWtalk page. The link text should be the student's full name.

Making Posts (Level 2)
Students should be able to make posts.
Searching Posts (Level 2)
It should be possible to search for posts containing particular words.
Commenting on Post and replying to Comments (Level 2)
When viewing a post, it should be possible to click on a link and create a comment on that post. When viewing a comment, it should be possible to click on a link and create a reply to that comment.
Friend/Unfriend Students (Level 3)
A student should be able to add & delete students from their friend list.
Pagination of Posts & Search Results (Level 3)
When searching for students or posts and when viewing posts the students be shown the first n (e.g n == 16) results. They should be able then view the next n and the next n and so on.
Student Account Creation (Level 3)
Your web site should allow students to create accounts with a zid, password and e-mail address. You should of course check that an account for this zid does not exist already. It should be compulsory that a valid e-mail-address is associated with an account but the e-mail address need not be a UNSW address.
You should confirm the e-mail address is valid and owned by the UNSWtalk student creating the account by e-mailing them a link necessary to complete account creation.

I expect (and recommend) most students to use the data format of the data set you've been supplied. If so for a new student you would need create a directory named with their zid and then add a appropriate student.txt containing their details.

Profile Text (Level 3)
A UNSWtalk student should be able to add to some text to their details, probably describing their interests, which is displayed with their student details.

My interests are long walks on the beach and Python programming.
I plan to use what I've learnt COMP9041 to cure the world of all known diseases.

It should be possible to use some simple (safe) HTML tags, and only these tags, in this text. The data set you've been given doesn't include any examples of such text.
You can choose to store this text in the student.txt file or elsewhere.

Friend Requests (Level 3)
A student, when viewing a UNSWtalk page, should be able to send a friend request to the owner of that UNSWtalk page. The other student should be notified by an e-mail. The e-mail should contain an appropriate link to the web site which will allow them to accept or reject the friend request.
Friend Suggestions (Level 3)
Your web site should be able to provide a list of likely friend suggestions.
Your web site should display UNSWtalk students sorted on how likely the student is to know them. It should display a set (say 10) of UNSWtalk students. It should allow the next best-matching set of potential friends or the previous set of potential friends to be viewed.

The student should be able to click on a potential friend, see their UNSWtalk page (where they will be able to send them a friend request).

Your matching algorithm should assume that people who have taken the same course in the same session may know each other.

For example Reese Witherspoon and James Franco are both taking 2017 S2 MATH1231 which should cause your algorithm to make Reese a more likely friend suggestion for James (and vice-versa).

Your matching algorithm should also assume that people may know friends of their friends.

You may choose to have your matching algorithm use other parts of student details.

Note there are many choices in this matching algorithm so your results will differ from other students. Be prepared to explain how & why your matching algorithm works during your assignment demo. You may chose to have a development mode available which when turned on displays extra information regarding the matching.

Password Recovery (Level 3)
Students should be able to recover/change lost passwords via having an e-mail sent to them.
Uploading & Deleting Images (Level 3)
In addition to their jpg image students should also be allowed to add a background image. A student should be able to upload/change/delete both background & profile images. The lecture CGI examples include one for uploading a file.
Editing Information (Level 3)
A student should be able to edit their details and change their profile images.
Deleting Posts (Level 3)
A UNSWtalk student should also be able to delete any of their posts, comments or replies.
Suspending/Deleting UNSWtalk Account (Level 3)
A UNSWtalk student not currently interested in UNSWtalk should be able to suspend their account. A suspended account is not visible to other students.
A UNSWtalk student should also be able to delete their account completely.

Notifications (Level 3)
A student should be able to indicate they wish to be notified by e-mail in one of these events:
their zid is mentioned in a post, comment or reply
they get a friend request
Including Links, Images & Videos (Level 3)
A student should be able to include links, images and videos in a post, comment or reply. These should be appropriately displayed when the item is viewed.
Privacy (Level 3)
A student should be able to make part or all of the content of their UNSWtalk page visible only to their friends.
Advanced Features (Level 4)
If you wish to obtain over 90% you should consider adding features beyond those above. Marks will be available for extra features.
Getting Started
