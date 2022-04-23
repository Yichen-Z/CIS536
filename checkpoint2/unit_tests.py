import navigate as nav
import mk_dict as m

# Create inverted index from sample of emails
# set HOME = r'C:\Users\house\Desktop\test'
m.make_index()

# Now let's go for the whole deal - clean and rewrite every email
# nav.navigate(nav.HOME)

# # test process for rewriting nested folder
# read = r'D:\cis_536\maildir\shackleton-s' # wow this person had folders
# nav.navigate(read)

# # test process for rewriting 1 folder
# read = r'D:\cis_536\maildir\saibi-e\discussion_threads'
# nav.navigate(read)

# # test process for rewriting 1 file with HTML formatting
# read_file = r'D:\cis_536\maildir\saibi-e\inbox\71'
# nav.process(read_file)

# # Test init_clean
# test_str = r"""Message-ID: <23282397.1075851677564.JavaMail.evans@thyme>
# Date: Sun, 26 Nov 2000 23:24:00 -0800 (PST)
# From: v.weldon@enron.com
# To: will.zapalac@bus.utexas.edu
# Subject: Re: Taite Zapalac - Welcome To The World
# Mime-Version: 1.0
# Content-Type: text/plain; charset=us-ascii
# Content-Transfer-Encoding: 7bit
# X-From: V Charles Weldon
# X-To: "Will Zapalac" <Will.Zapalac@bus.utexas.edu> @ ENRON
# X-cc: 
# X-bcc: 
# X-Folder: \Charles_Wheldon_Nov2001\Notes Folders\All documents
# X-Origin: WHELDON-C
# X-FileName: vweldon.nsf

# Congratualtions, Will!  May God bless you and your family.  She's a beautiful 
# baby.

# How is recruiting going?   Any idea where you think you will end up.  I'm 
# sorry it did not work out at Enron.  I know that you will do well wherever 
# you go.


# Charlie"""
# print(nav.init_clean(nav.clean, test_str))

# # Test get_docID
# test_str = r"""Message-ID: <23282397.1075851677564.JavaMail.evans@thyme>
# Date: Sun, 26 Nov 2000 23:24:00 -0800 (PST)"""
# print(nav.get_docID(nav.messageID, test_str))