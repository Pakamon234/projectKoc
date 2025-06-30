USE [KOC]
GO
/****** Object:  Table [dbo].[business]    Script Date: 6/8/2025 10:11:55 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[business](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[name] [nvarchar](50) NOT NULL,
	[address] [nvarchar](50) NOT NULL,
	[email] [nvarchar](50) NOT NULL,
	[phoneNumber] [nchar](10) NOT NULL,
	[website] [nvarchar](256) NULL,
	[authenticate] [bit] NULL,
	[createdAt] [datetime] NULL,
	[updatedAt] [datetime] NULL,
	[userId] [nchar](32) NULL,
	[status] [nvarchar](50) NULL,
 CONSTRAINT [PK_Adviser] PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[campaign]    Script Date: 6/8/2025 10:11:55 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[campaign](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[businessId] [int] NOT NULL,
	[campaignCategoryId] [int] NOT NULL,
	[title] [nvarchar](50) NOT NULL,
	[description] [nvarchar](max) NULL,
	[thumbnail] [nvarchar](256) NULL,
	[startDate] [date] NOT NULL,
	[endDate] [date] NOT NULL,
	[registerStartDate] [date] NOT NULL,
	[registerEndDate] [date] NOT NULL,
	[numberOfParticipants] [int] NOT NULL,
	[status] [int] NULL,
	[createdAt] [datetime] NULL,
	[updatedAt] [datetime] NULL,
	[isConfirmed] [int] NULL,
 CONSTRAINT [PK_Campaign] PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO
/****** Object:  Table [dbo].[campaignCategory]    Script Date: 6/8/2025 10:11:55 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[campaignCategory](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[name] [nvarchar](50) NULL,
	[description] [nvarchar](250) NULL,
 CONSTRAINT [PK_Campaign_category] PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[campaignProduct]    Script Date: 6/8/2025 10:11:55 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[campaignProduct](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[campaignId] [int] NOT NULL,
	[productId] [int] NOT NULL,
	[commission] [float] NOT NULL,
 CONSTRAINT [PK_Campaign_product_1] PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[commission]    Script Date: 6/8/2025 10:11:55 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[commission](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[registerId] [int] NOT NULL,
	[quantity] [int] NULL,
	[amount] [int] NULL,
	[totalAmount] [int] NULL,
	[commissionMoney] [float] NULL,
	[isDone] [bit] NULL,
 CONSTRAINT [PK_Commission] PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[employee]    Script Date: 6/8/2025 10:11:55 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[employee](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[name] [nvarchar](50) NOT NULL,
	[dob] [date] NOT NULL,
	[gender] [nvarchar](3) NOT NULL,
	[email] [nvarchar](50) NOT NULL,
	[address] [nvarchar](50) NOT NULL,
	[phoneNumber] [nchar](10) NOT NULL,
	[picture] [nvarchar](250) NULL,
	[userId] [nchar](32) NULL,
	[status] [nvarchar](20) NULL,
	[updatedAt] [datetime] NULL,
	[createdAt] [datetime] NULL,
 CONSTRAINT [PK_Admin] PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[koc]    Script Date: 6/8/2025 10:11:55 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[koc](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[dob] [date] NOT NULL,
	[bio] [nvarchar](200) NULL,
	[socialLink] [nvarchar](256) NULL,
	[name] [nvarchar](64) NOT NULL,
	[gender] [nvarchar](3) NOT NULL,
	[email] [nvarchar](50) NULL,
	[phoneNumber] [nchar](10) NULL,
	[address] [nvarchar](50) NULL,
	[picture] [nvarchar](255) NULL,
	[isKoc] [bit] NULL,
	[kocConfirmDate] [datetime] NULL,
	[createdAt] [datetime] NULL,
	[updatedAt] [datetime] NULL,
	[userId] [nchar](32) NULL,
	[status] [nvarchar](50) NULL,
 CONSTRAINT [PK_KOC] PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[orderDetail]    Script Date: 6/8/2025 10:11:55 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[orderDetail](
	[orderId] [int] NOT NULL,
	[productId] [int] NOT NULL,
	[quantity] [int] NOT NULL,
	[amountPerOne] [int] NOT NULL,
	[totalAmount] [int] NOT NULL,
	[kocCode] [nchar](10) NULL,
	[rating] [int] NULL,
	[comment] [nvarchar](max) NULL,
 CONSTRAINT [PK_orderDetail] PRIMARY KEY CLUSTERED 
(
	[orderId] ASC,
	[productId] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO
/****** Object:  Table [dbo].[orderPro]    Script Date: 6/8/2025 10:11:55 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[orderPro](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[kocId] [int] NOT NULL,
	[orderDate] [datetime] NOT NULL,
	[totalPrice] [int] NULL,
	[isPay] [bit] NULL,
	[payDate] [datetime] NULL,
	[orderStatus] [nvarchar](50) NULL,
	[address] [nvarchar](256) NULL,
	[reasonCancel] [nvarchar](64) NULL,
 CONSTRAINT [PK_orderPro] PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[proCate]    Script Date: 6/8/2025 10:11:55 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[proCate](
	[productId] [int] NOT NULL,
	[productCategoryId] [int] NOT NULL,
 CONSTRAINT [PK_Pro_cate] PRIMARY KEY CLUSTERED 
(
	[productId] ASC,
	[productCategoryId] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[product]    Script Date: 6/8/2025 10:11:55 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[product](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[name] [nvarchar](50) NOT NULL,
	[createdAt] [datetime] NULL,
	[updatedAt] [datetime] NULL,
 CONSTRAINT [PK_Product] PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[productBusinees]    Script Date: 6/8/2025 10:11:55 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[productBusinees](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[productId] [int] NOT NULL,
	[businessId] [int] NOT NULL,
	[title] [nvarchar](128) NULL,
	[image] [nvarchar](256) NULL,
	[unitOfMeasure] [nvarchar](10) NULL,
	[description] [nvarchar](max) NULL,
	[amount] [int] NULL,
	[quantityInStock] [int] NULL,
	[rating] [float] NULL,
	[updatedAt] [datetime] NULL,
	[createdAt] [datetime] NULL,
 CONSTRAINT [PK_productBusinees] PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO
/****** Object:  Table [dbo].[productCategory]    Script Date: 6/8/2025 10:11:55 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[productCategory](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[name] [nvarchar](50) NULL,
 CONSTRAINT [PK_Product_category] PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[registerCampaign]    Script Date: 6/8/2025 10:11:55 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[registerCampaign](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[kocId] [int] NOT NULL,
	[campaign_product_id] [int] NOT NULL,
	[registerDate] [datetime] NOT NULL,
	[status] [nvarchar](50) NOT NULL,
	[kocCode] [nchar](10) NULL,
	[kocCodeValue] [float] NULL,
 CONSTRAINT [PK_Register_campaign_1] PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[reviewDetails]    Script Date: 6/8/2025 10:11:55 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[reviewDetails](
	[reviewId] [int] NOT NULL,
	[kocId] [int] NOT NULL,
	[text] [nvarchar](max) NULL,
	[rating] [int] NULL,
	[date] [datetime] NULL,
 CONSTRAINT [PK_reviewDetails] PRIMARY KEY CLUSTERED 
(
	[reviewId] ASC,
	[kocId] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Reviews]    Script Date: 6/8/2025 10:11:55 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Reviews](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[registerId] [int] NOT NULL,
	[rating] [float] NULL,
	[text] [nvarchar](max) NOT NULL,
	[createdAt] [datetime] NULL,
	[updatedAt] [datetime] NULL,
 CONSTRAINT [PK_Reviews] PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO
/****** Object:  Table [dbo].[role]    Script Date: 6/8/2025 10:11:55 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[role](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[name] [nvarchar](50) NULL,
	[description] [nvarchar](50) NULL,
 CONSTRAINT [PK_Role] PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[roleDetails]    Script Date: 6/8/2025 10:11:55 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[roleDetails](
	[roleId] [int] NOT NULL,
	[functionId] [int] NOT NULL,
 CONSTRAINT [PK_roleDetails] PRIMARY KEY CLUSTERED 
(
	[roleId] ASC,
	[functionId] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[roleFunction]    Script Date: 6/8/2025 10:11:55 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[roleFunction](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[name] [nvarchar](50) NULL,
	[description] [nvarchar](50) NULL,
 CONSTRAINT [PK_Role_function] PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[User]    Script Date: 6/8/2025 10:11:55 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[User](
	[userName] [nchar](32) NOT NULL,
	[password] [nchar](64) NOT NULL,
	[roleId] [int] NOT NULL,
	[createdAt] [datetime] NULL,
	[updatedAt] [datetime] NULL,
	[authenticate] [bit] NULL,
	[status] [nvarchar](50) NULL,
 CONSTRAINT [PK_User_1] PRIMARY KEY CLUSTERED 
(
	[userName] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
SET IDENTITY_INSERT [dbo].[business] ON 
GO
INSERT [dbo].[business] ([id], [name], [address], [email], [phoneNumber], [website], [authenticate], [createdAt], [updatedAt], [userId], [status]) VALUES (1, N'Công ty XY', N'quận 9', N'nguyenthanhlong091103@gmail.com', N'0327180211', N'https://www.youtube.com/watch?v=As7xZO-WiUs&list=RDAs7xZO-WiUs&start_radio=1', 1, CAST(N'2025-04-08T08:12:49.527' AS DateTime), CAST(N'2025-04-23T16:44:30.673' AS DateTime), N'doanhnghiep1                    ', N'Còn')
GO
INSERT [dbo].[business] ([id], [name], [address], [email], [phoneNumber], [website], [authenticate], [createdAt], [updatedAt], [userId], [status]) VALUES (5, N'Công ty Mỹ Phẩm CBA', N'quận 9', N'testneheff@gmail.com', N'0327180211', N'', 1, CAST(N'2025-04-18T02:17:26.567' AS DateTime), CAST(N'2025-04-22T15:00:06.927' AS DateTime), N'doanhnghiep5                    ', N'còn')
GO
INSERT [dbo].[business] ([id], [name], [address], [email], [phoneNumber], [website], [authenticate], [createdAt], [updatedAt], [userId], [status]) VALUES (7, N'Cửa hàng', N'Tp.Thủ Đức', N'nguyenthanhlong091103@gmail.com', N'0327180211', N'', 1, CAST(N'2025-04-24T09:09:04.970' AS DateTime), CAST(N'2025-04-24T09:09:25.297' AS DateTime), NULL, N'còn')
GO
SET IDENTITY_INSERT [dbo].[business] OFF
GO
SET IDENTITY_INSERT [dbo].[campaign] ON 
GO
INSERT [dbo].[campaign] ([id], [businessId], [campaignCategoryId], [title], [description], [thumbnail], [startDate], [endDate], [registerStartDate], [registerEndDate], [numberOfParticipants], [status], [createdAt], [updatedAt], [isConfirmed]) VALUES (2, 1, 1, N'Thời trang rực rỡ', N'Mùa này, chúng tôi mang đến chiến dịch “RỰC RỠ” – nơi thời trang không chỉ là quần áo, mà là tuyên ngôn cá nhân. Lấy cảm hứng từ những gam màu sống động, hoa văn táo bạo và những đường cắt phóng khoáng, “RỰC RỠ” tôn vinh vẻ đẹp đa dạng và tinh thần tự do của thế hệ hiện đại.

Từ sàn diễn ra phố phường, mỗi bộ trang phục là một điểm nhấn khiến bạn không thể bị lu mờ. Đây không chỉ là sự lựa chọn phong cách – đây là cách bạn nói với thế giới: Tôi ở đây, và tôi rực rỡ theo cách của riêng mình.

Hãy sẵn sàng bùng nổ cá tính cùng chúng tôi!
📍#RucRoFashion #ToaSangCungStyle #LiveInColor', NULL, CAST(N'2025-04-24' AS Date), CAST(N'2025-06-01' AS Date), CAST(N'2025-04-09' AS Date), CAST(N'2025-04-24' AS Date), 1, 2, CAST(N'2025-04-08T21:48:07.307' AS DateTime), CAST(N'2025-04-23T17:06:14.150' AS DateTime), 3)
GO
INSERT [dbo].[campaign] ([id], [businessId], [campaignCategoryId], [title], [description], [thumbnail], [startDate], [endDate], [registerStartDate], [registerEndDate], [numberOfParticipants], [status], [createdAt], [updatedAt], [isConfirmed]) VALUES (4, 1, 2, N'Thời trang nhiệm màu', N'Thời trang nhiệm màu là hành trình vượt qua những ranh giới thường nhật, nơi trang phục không chỉ để mặc mà còn là phép màu kể chuyện. Mỗi chi tiết – từ ánh kim lấp lánh, chất liệu bay bổng đến bảng màu huyền ảo – đều gợi mở một thế giới mộng mơ và siêu thực.

Lấy cảm hứng từ cổ tích, thiên nhiên kỳ ảo hay vũ trụ huyền bí, phong cách này hòa quyện giữa thực tại và tưởng tượng. Váy áo như thoát ra từ một giấc mơ, nơi nàng tiên, pháp sư, hay những linh hồn cổ xưa bước vào đời thường với nét quyến rũ ma mị.

Thời trang nhiệm màu không chỉ là xu hướng – đó là cảm xúc, là cách bạn biến mỗi ngày thành một điều kỳ diệu đáng nhớ.', NULL, CAST(N'2025-05-23' AS Date), CAST(N'2025-06-01' AS Date), CAST(N'2025-04-22' AS Date), CAST(N'2025-04-27' AS Date), 2, 0, CAST(N'2025-04-22T05:37:11.177' AS DateTime), CAST(N'2025-04-23T17:10:07.043' AS DateTime), NULL)
GO
INSERT [dbo].[campaign] ([id], [businessId], [campaignCategoryId], [title], [description], [thumbnail], [startDate], [endDate], [registerStartDate], [registerEndDate], [numberOfParticipants], [status], [createdAt], [updatedAt], [isConfirmed]) VALUES (11, 1, 2, N'Chiến dịch 2025', N'Chiến dịch "Chiến dịch 2025" được xây dựng nhằm giới thiệu đa dạng các dòng sản phẩm từ thương hiệu, mang đến cho người tiêu dùng trải nghiệm toàn diện về chất lượng, phong cách và công dụng. Từ các sản phẩm chăm sóc cá nhân, thời trang, gia dụng đến thực phẩm tiện lợi – mỗi sản phẩm là một câu chuyện, một lựa chọn phù hợp với từng phong cách sống riêng biệt.

Chiến dịch kết hợp nhiều hình thức truyền thông như review KOC, livestream trải nghiệm thực tế, mini game tương tác trên mạng xã hội, cùng các ưu đãi giới hạn thời gian để khuyến khích hành vi mua sắm và tăng độ nhận diện thương hiệu.', NULL, CAST(N'2025-01-01' AS Date), CAST(N'2025-12-31' AS Date), CAST(N'2025-01-01' AS Date), CAST(N'2025-06-01' AS Date), 1000, 2, CAST(N'2024-12-31T00:00:00.000' AS DateTime), CAST(N'2024-12-31T00:00:00.000' AS DateTime), 3)
GO
INSERT [dbo].[campaign] ([id], [businessId], [campaignCategoryId], [title], [description], [thumbnail], [startDate], [endDate], [registerStartDate], [registerEndDate], [numberOfParticipants], [status], [createdAt], [updatedAt], [isConfirmed]) VALUES (12, 5, 2, N'Kết nối Người tiêu dùng', N'Kết nối người tiêu dùng và nhà cung cấp', NULL, CAST(N'2025-06-01' AS Date), CAST(N'2025-08-01' AS Date), CAST(N'2025-05-01' AS Date), CAST(N'2025-05-20' AS Date), 10, 5, CAST(N'2025-04-24T06:33:30.140' AS DateTime), CAST(N'2025-04-24T09:15:28.090' AS DateTime), NULL)
GO
INSERT [dbo].[campaign] ([id], [businessId], [campaignCategoryId], [title], [description], [thumbnail], [startDate], [endDate], [registerStartDate], [registerEndDate], [numberOfParticipants], [status], [createdAt], [updatedAt], [isConfirmed]) VALUES (13, 1, 2, N'Mùa hè năm 2024', N'Mùa hè năm 2024', NULL, CAST(N'2025-04-25' AS Date), CAST(N'2025-06-28' AS Date), CAST(N'2025-04-21' AS Date), CAST(N'2025-04-27' AS Date), 2, 2, CAST(N'2025-04-24T09:13:17.173' AS DateTime), CAST(N'2025-04-24T09:15:03.703' AS DateTime), 3)
GO
SET IDENTITY_INSERT [dbo].[campaign] OFF
GO
SET IDENTITY_INSERT [dbo].[campaignCategory] ON 
GO
INSERT [dbo].[campaignCategory] ([id], [name], [description]) VALUES (1, N'Ra mắt sản phẩm mới', N'Giới thiệu sản phẩm/mẫu mã mới ra thị trường')
GO
INSERT [dbo].[campaignCategory] ([id], [name], [description]) VALUES (2, N'Chiến dịch theo mùa', N'Dịp lễ hội: Tết, Valentine, Trung thu, Back to School,')
GO
INSERT [dbo].[campaignCategory] ([id], [name], [description]) VALUES (3, N'Lan toả thương hiệu', N'Tăng nhận diện thương hiệu thông qua chia sẻ rộng rãi')
GO
INSERT [dbo].[campaignCategory] ([id], [name], [description]) VALUES (4, N'Quảng bá sản phẩm dịp đặc biệt', N'Ví dụ: mừng sinh nhật thương hiệu, 11.11, Black Friday, Tết,...')
GO
SET IDENTITY_INSERT [dbo].[campaignCategory] OFF
GO
SET IDENTITY_INSERT [dbo].[campaignProduct] ON 
GO
INSERT [dbo].[campaignProduct] ([id], [campaignId], [productId], [commission]) VALUES (10, 2, 3, 0.02)
GO
INSERT [dbo].[campaignProduct] ([id], [campaignId], [productId], [commission]) VALUES (11, 2, 2, 0.02)
GO
INSERT [dbo].[campaignProduct] ([id], [campaignId], [productId], [commission]) VALUES (13, 11, 2, 0.02)
GO
INSERT [dbo].[campaignProduct] ([id], [campaignId], [productId], [commission]) VALUES (14, 11, 3, 0.02)
GO
INSERT [dbo].[campaignProduct] ([id], [campaignId], [productId], [commission]) VALUES (15, 12, 4, 0.05)
GO
INSERT [dbo].[campaignProduct] ([id], [campaignId], [productId], [commission]) VALUES (16, 12, 5, 0.05)
GO
INSERT [dbo].[campaignProduct] ([id], [campaignId], [productId], [commission]) VALUES (17, 13, 2, 0.02)
GO
INSERT [dbo].[campaignProduct] ([id], [campaignId], [productId], [commission]) VALUES (18, 13, 3, 0.02)
GO
SET IDENTITY_INSERT [dbo].[campaignProduct] OFF
GO
SET IDENTITY_INSERT [dbo].[employee] ON 
GO
INSERT [dbo].[employee] ([id], [name], [dob], [gender], [email], [address], [phoneNumber], [picture], [userId], [status], [updatedAt], [createdAt]) VALUES (3, N'Nguyễn Thành Long', CAST(N'2003-09-11' AS Date), N'Nam', N'ttgddtn05111@gmail.com', N'Đắk Lắk', N'0327180211', NULL, N'nhanvien1                       ', N'Đang làm', CAST(N'2025-04-24T06:28:15.600' AS DateTime), CAST(N'2025-04-22T15:11:57.750' AS DateTime))
GO
SET IDENTITY_INSERT [dbo].[employee] OFF
GO
SET IDENTITY_INSERT [dbo].[koc] ON 
GO
INSERT [dbo].[koc] ([id], [dob], [bio], [socialLink], [name], [gender], [email], [phoneNumber], [address], [picture], [isKoc], [kocConfirmDate], [createdAt], [updatedAt], [userId], [status]) VALUES (18, CAST(N'2003-11-09' AS Date), N'nguời eww', N'https://www.youtube.com/watch?v=As7xZO-WiUs&list=RDAs7xZO-WiUs&start_radio=1', N'Nguyễn Thành Long', N'Nam', N'nguyenthanhlong091103@gmail.com', N'0327180211', N'Quận 9', N'474793145_1388785572438800_3107484666986752607_n.jpg', 1, CAST(N'2025-04-22T00:00:00.000' AS DateTime), CAST(N'2025-04-08T08:08:25.983' AS DateTime), CAST(N'2025-04-24T00:31:13.423' AS DateTime), N'pakamon                         ', N'còn')
GO
INSERT [dbo].[koc] ([id], [dob], [bio], [socialLink], [name], [gender], [email], [phoneNumber], [address], [picture], [isKoc], [kocConfirmDate], [createdAt], [updatedAt], [userId], [status]) VALUES (29, CAST(N'2000-01-01' AS Date), NULL, NULL, N'Ngô Thành An', N'Nam', N'nguyenthanhlong091103@gmail.com', N'0327180211', N'Tp.Thủ Đức', NULL, 1, CAST(N'2025-04-24T03:06:32.390' AS DateTime), CAST(N'2025-04-23T11:26:52.170' AS DateTime), CAST(N'2025-04-23T11:26:52.170' AS DateTime), N'nguoitieudung02                 ', N'còn')
GO
INSERT [dbo].[koc] ([id], [dob], [bio], [socialLink], [name], [gender], [email], [phoneNumber], [address], [picture], [isKoc], [kocConfirmDate], [createdAt], [updatedAt], [userId], [status]) VALUES (32, CAST(N'2001-02-09' AS Date), N'Người mới', N'None', N'Trần Thế Anh', N'Nam', N'nejape8345@agiuse.com', N'0327180211', N'Quận 1', N'tai_xuong_19.jpg', 1, CAST(N'2025-04-24T06:21:28.160' AS DateTime), CAST(N'2025-04-24T06:20:09.243' AS DateTime), CAST(N'2025-04-24T06:21:23.463' AS DateTime), N'nguoitieudung03                 ', N'còn')
GO
INSERT [dbo].[koc] ([id], [dob], [bio], [socialLink], [name], [gender], [email], [phoneNumber], [address], [picture], [isKoc], [kocConfirmDate], [createdAt], [updatedAt], [userId], [status]) VALUES (34, CAST(N'2000-02-05' AS Date), NULL, NULL, N'Nguyễn Trung Nguyên', N'Nam', N'nejape8345@agiuse.com', N'0327180211', N'Quận 7', NULL, NULL, NULL, CAST(N'2025-04-24T08:58:08.427' AS DateTime), CAST(N'2025-04-24T08:58:08.427' AS DateTime), N'nguoitieudung04                 ', N'còn')
GO
INSERT [dbo].[koc] ([id], [dob], [bio], [socialLink], [name], [gender], [email], [phoneNumber], [address], [picture], [isKoc], [kocConfirmDate], [createdAt], [updatedAt], [userId], [status]) VALUES (35, CAST(N'2000-01-01' AS Date), N'Người mới', N'http://127.0.0.1:5000/dashboard/koc/edit', N'NGô An', N'Nữ', N'capiya8630@agiuse.com', N'0327180211', N'Quận 7', N'image2.jpg', 1, CAST(N'2025-04-24T09:03:09.980' AS DateTime), CAST(N'2025-04-24T09:01:02.050' AS DateTime), CAST(N'2025-04-24T09:02:52.953' AS DateTime), N'nguoitieudung05                 ', N'còn')
GO
SET IDENTITY_INSERT [dbo].[koc] OFF
GO
INSERT [dbo].[orderDetail] ([orderId], [productId], [quantity], [amountPerOne], [totalAmount], [kocCode], [rating], [comment]) VALUES (1, 2, 2, 250000, 500000, NULL, 5, N'Tuyệt')
GO
INSERT [dbo].[orderDetail] ([orderId], [productId], [quantity], [amountPerOne], [totalAmount], [kocCode], [rating], [comment]) VALUES (2, 2, 1, 250000, 242500, N'T4aDu4qxfZ', NULL, NULL)
GO
INSERT [dbo].[orderDetail] ([orderId], [productId], [quantity], [amountPerOne], [totalAmount], [kocCode], [rating], [comment]) VALUES (2, 3, 2, 500000, 980000, N'PEzViASD57', NULL, NULL)
GO
INSERT [dbo].[orderDetail] ([orderId], [productId], [quantity], [amountPerOne], [totalAmount], [kocCode], [rating], [comment]) VALUES (3, 2, 3, 250000, 727500, N'T4aDu4qxfZ', 5, N'Đẹp')
GO
SET IDENTITY_INSERT [dbo].[orderPro] ON 
GO
INSERT [dbo].[orderPro] ([id], [kocId], [orderDate], [totalPrice], [isPay], [payDate], [orderStatus], [address], [reasonCancel]) VALUES (1, 18, CAST(N'2025-04-20T22:20:18.003' AS DateTime), 500000, 1, CAST(N'2025-04-24T00:00:00.000' AS DateTime), N'Đơn thành công', N'quận 9', NULL)
GO
INSERT [dbo].[orderPro] ([id], [kocId], [orderDate], [totalPrice], [isPay], [payDate], [orderStatus], [address], [reasonCancel]) VALUES (2, 18, CAST(N'2025-04-20T00:14:13.733' AS DateTime), 1222500, 0, CAST(N'2025-04-24T00:00:00.000' AS DateTime), N'Đơn thành công', N'Tp.Thủ Đức', NULL)
GO
INSERT [dbo].[orderPro] ([id], [kocId], [orderDate], [totalPrice], [isPay], [payDate], [orderStatus], [address], [reasonCancel]) VALUES (3, 18, CAST(N'2025-04-24T09:23:18.193' AS DateTime), 727500, 0, CAST(N'2025-04-24T16:25:00.000' AS DateTime), N'Đơn thành công', N'Quận 1', NULL)
GO
SET IDENTITY_INSERT [dbo].[orderPro] OFF
GO
INSERT [dbo].[proCate] ([productId], [productCategoryId]) VALUES (1, 1)
GO
INSERT [dbo].[proCate] ([productId], [productCategoryId]) VALUES (3, 4)
GO
INSERT [dbo].[proCate] ([productId], [productCategoryId]) VALUES (3, 6)
GO
INSERT [dbo].[proCate] ([productId], [productCategoryId]) VALUES (5, 1)
GO
INSERT [dbo].[proCate] ([productId], [productCategoryId]) VALUES (5, 5)
GO
INSERT [dbo].[proCate] ([productId], [productCategoryId]) VALUES (6, 5)
GO
INSERT [dbo].[proCate] ([productId], [productCategoryId]) VALUES (6, 8)
GO
INSERT [dbo].[proCate] ([productId], [productCategoryId]) VALUES (7, 2)
GO
INSERT [dbo].[proCate] ([productId], [productCategoryId]) VALUES (7, 7)
GO
INSERT [dbo].[proCate] ([productId], [productCategoryId]) VALUES (8, 1)
GO
INSERT [dbo].[proCate] ([productId], [productCategoryId]) VALUES (8, 5)
GO
INSERT [dbo].[proCate] ([productId], [productCategoryId]) VALUES (9, 3)
GO
INSERT [dbo].[proCate] ([productId], [productCategoryId]) VALUES (10, 4)
GO
INSERT [dbo].[proCate] ([productId], [productCategoryId]) VALUES (11, 9)
GO
INSERT [dbo].[proCate] ([productId], [productCategoryId]) VALUES (12, 3)
GO
INSERT [dbo].[proCate] ([productId], [productCategoryId]) VALUES (12, 5)
GO
INSERT [dbo].[proCate] ([productId], [productCategoryId]) VALUES (13, 2)
GO
INSERT [dbo].[proCate] ([productId], [productCategoryId]) VALUES (13, 6)
GO
SET IDENTITY_INSERT [dbo].[product] ON 
GO
INSERT [dbo].[product] ([id], [name], [createdAt], [updatedAt]) VALUES (1, N'Đồ bộ 7 sắc cầu vòng', CAST(N'2025-04-09T01:40:51.273' AS DateTime), CAST(N'2025-04-23T09:53:58.083' AS DateTime))
GO
INSERT [dbo].[product] ([id], [name], [createdAt], [updatedAt]) VALUES (3, N'Kem dưỡng ẩm KOLS', CAST(N'2025-04-09T01:40:51.273' AS DateTime), CAST(N'2025-04-23T09:54:10.043' AS DateTime))
GO
INSERT [dbo].[product] ([id], [name], [createdAt], [updatedAt]) VALUES (5, N'Balo Laptop', CAST(N'2025-04-23T09:54:38.353' AS DateTime), NULL)
GO
INSERT [dbo].[product] ([id], [name], [createdAt], [updatedAt]) VALUES (6, N'Đèn bàn', CAST(N'2025-04-24T06:24:56.220' AS DateTime), NULL)
GO
INSERT [dbo].[product] ([id], [name], [createdAt], [updatedAt]) VALUES (7, N'Sữa', CAST(N'2025-04-24T06:25:08.763' AS DateTime), NULL)
GO
INSERT [dbo].[product] ([id], [name], [createdAt], [updatedAt]) VALUES (8, N'Đồng hồ thông minh', CAST(N'2025-04-24T06:26:05.120' AS DateTime), NULL)
GO
INSERT [dbo].[product] ([id], [name], [createdAt], [updatedAt]) VALUES (9, N'Nồi cơm điện', CAST(N'2025-04-24T06:26:20.267' AS DateTime), NULL)
GO
INSERT [dbo].[product] ([id], [name], [createdAt], [updatedAt]) VALUES (10, N'Gel chống nắng', CAST(N'2025-04-24T06:27:01.743' AS DateTime), NULL)
GO
INSERT [dbo].[product] ([id], [name], [createdAt], [updatedAt]) VALUES (11, N'Sách dạy nấu ăn', CAST(N'2025-04-24T06:27:20.917' AS DateTime), CAST(N'2025-04-24T06:27:37.260' AS DateTime))
GO
INSERT [dbo].[product] ([id], [name], [createdAt], [updatedAt]) VALUES (12, N'Cân điện tử', CAST(N'2025-04-24T06:29:11.733' AS DateTime), NULL)
GO
INSERT [dbo].[product] ([id], [name], [createdAt], [updatedAt]) VALUES (13, N'Viên uống Vitamin A', CAST(N'2025-04-24T06:29:35.753' AS DateTime), NULL)
GO
SET IDENTITY_INSERT [dbo].[product] OFF
GO
SET IDENTITY_INSERT [dbo].[productBusinees] ON 
GO
INSERT [dbo].[productBusinees] ([id], [productId], [businessId], [title], [image], [unitOfMeasure], [description], [amount], [quantityInStock], [rating], [updatedAt], [createdAt]) VALUES (2, 1, 1, N'Đồ bộ 7 màu kỳ lân', N'1949e29aa73fec32cbaa7cbbde2975aa.jpg', N'bộ', N'Bộ đồ trong ảnh là một bộ đồ ngủ (onesie) kỳ lân bảy màu, nổi bật và dễ thương, thường được ưa chuộng trong các dịp ở nhà thư giãn, cosplay, tiệc pyjama hoặc chụp ảnh

Mô tả chi tiết:
Thiết kế: Nguyên bộ liền thân, có mũ trùm đầu hình đầu kỳ lân.

Họa tiết: Phối màu cầu vồng rực rỡ với các tông màu hồng, vàng, xanh dương, xanh lá, tím... tạo hiệu ứng bắt mắt và vui nhộn.

Chất liệu: Vải nỉ bông mềm mịn, tạo cảm giác ấm áp, dễ chịu khi mặc.

Mũ trùm đầu: Hình đầu kỳ lân với chi tiết sừng màu vàng, tai hồng và đôi mắt tròn to cực kỳ đáng yêu.

Phần chân: Có kèm dép hoặc bọc chân hình móng kỳ lân màu vàng nổi bật.

Phong cách: Dễ thương, năng động, phù hợp với người yêu thích phong cách hoạt hình và kỳ lân huyền thoại.', 250000, 113, 5, CAST(N'2025-04-23T10:18:43.250' AS DateTime), CAST(N'2025-04-09T02:01:51.280' AS DateTime))
GO
INSERT [dbo].[productBusinees] ([id], [productId], [businessId], [title], [image], [unitOfMeasure], [description], [amount], [quantityInStock], [rating], [updatedAt], [createdAt]) VALUES (3, 3, 1, N'Dưỡng ẩm Đêm', N'tai_xuong_19.jpg', N'hũ', N'xxxx', 500000, 200, NULL, CAST(N'2025-04-23T16:48:25.143' AS DateTime), CAST(N'2025-04-23T16:48:25.143' AS DateTime))
GO
INSERT [dbo].[productBusinees] ([id], [productId], [businessId], [title], [image], [unitOfMeasure], [description], [amount], [quantityInStock], [rating], [updatedAt], [createdAt]) VALUES (4, 10, 5, N'Gel chống nắng Swim', N'gelchongnang.jpg', N'chai', N'Gel chống nắng chống UV cực mạnh', 320000, 100, NULL, CAST(N'2025-04-24T06:44:08.353' AS DateTime), CAST(N'2025-04-24T06:44:08.353' AS DateTime))
GO
INSERT [dbo].[productBusinees] ([id], [productId], [businessId], [title], [image], [unitOfMeasure], [description], [amount], [quantityInStock], [rating], [updatedAt], [createdAt]) VALUES (5, 6, 5, N'Đèn bàn chống cận', N'denban.jpg', N'cái', N'Đèn bàn hiện đại, hỗ trợ chống cận', 120000, 10, NULL, CAST(N'2025-04-24T06:47:42.573' AS DateTime), CAST(N'2025-04-24T06:47:42.573' AS DateTime))
GO
SET IDENTITY_INSERT [dbo].[productBusinees] OFF
GO
SET IDENTITY_INSERT [dbo].[productCategory] ON 
GO
INSERT [dbo].[productCategory] ([id], [name]) VALUES (1, N'Thời trang')
GO
INSERT [dbo].[productCategory] ([id], [name]) VALUES (2, N'Thực phẩm & Đồ uống')
GO
INSERT [dbo].[productCategory] ([id], [name]) VALUES (3, N'Gia dụng')
GO
INSERT [dbo].[productCategory] ([id], [name]) VALUES (4, N'Mỹ phẩm')
GO
INSERT [dbo].[productCategory] ([id], [name]) VALUES (5, N'Thiết bị điện tử')
GO
INSERT [dbo].[productCategory] ([id], [name]) VALUES (6, N'Sức khỏe & Thể thao')
GO
INSERT [dbo].[productCategory] ([id], [name]) VALUES (7, N'Mẹ & Bé')
GO
INSERT [dbo].[productCategory] ([id], [name]) VALUES (8, N'Văn phòng phẩm')
GO
INSERT [dbo].[productCategory] ([id], [name]) VALUES (9, N'Sách và Tài liệu')
GO
SET IDENTITY_INSERT [dbo].[productCategory] OFF
GO
SET IDENTITY_INSERT [dbo].[registerCampaign] ON 
GO
INSERT [dbo].[registerCampaign] ([id], [kocId], [campaign_product_id], [registerDate], [status], [kocCode], [kocCodeValue]) VALUES (9, 18, 10, CAST(N'2025-04-23T17:24:33.477' AS DateTime), N'Thất bại', NULL, NULL)
GO
INSERT [dbo].[registerCampaign] ([id], [kocId], [campaign_product_id], [registerDate], [status], [kocCode], [kocCodeValue]) VALUES (11, 18, 11, CAST(N'2025-04-23T17:26:23.023' AS DateTime), N'Thành công', N'UWiJ6eSyCS', 0.02)
GO
INSERT [dbo].[registerCampaign] ([id], [kocId], [campaign_product_id], [registerDate], [status], [kocCode], [kocCodeValue]) VALUES (12, 18, 13, CAST(N'2025-04-23T22:54:06.037' AS DateTime), N'Thành công', N'T4aDu4qxfZ', 0.03)
GO
INSERT [dbo].[registerCampaign] ([id], [kocId], [campaign_product_id], [registerDate], [status], [kocCode], [kocCodeValue]) VALUES (13, 18, 14, CAST(N'2025-04-24T00:09:21.897' AS DateTime), N'Thành công', N'PEzViASD57', 0.02)
GO
INSERT [dbo].[registerCampaign] ([id], [kocId], [campaign_product_id], [registerDate], [status], [kocCode], [kocCodeValue]) VALUES (14, 18, 18, CAST(N'2025-04-24T09:16:27.510' AS DateTime), N'Thành công', N'DHOlR16zgs', 0.05)
GO
SET IDENTITY_INSERT [dbo].[registerCampaign] OFF
GO
INSERT [dbo].[reviewDetails] ([reviewId], [kocId], [text], [rating], [date]) VALUES (2, 18, N'ổn', 5, CAST(N'2025-04-25T00:00:00.000' AS DateTime))
GO
INSERT [dbo].[reviewDetails] ([reviewId], [kocId], [text], [rating], [date]) VALUES (3, 18, N'Thật bổ ích', 5, NULL)
GO
SET IDENTITY_INSERT [dbo].[Reviews] ON 
GO
INSERT [dbo].[Reviews] ([id], [registerId], [rating], [text], [createdAt], [updatedAt]) VALUES (2, 11, 5, N'🌈✨ Review Đồ Bộ Kỳ Lân 7 Màu – Mặc Là “Auto Cute” ✨🌈
Nếu bạn đang cần tìm một bộ đồ vừa dễ thương, vừa thoải mái để mặc ở nhà hay đi chơi nhẹ nhàng thì... đồ bộ kỳ lân 7 màu là chân ái! 🦄💖

🧁 Ấn tượng đầu tiên:
Màu sắc rực rỡ 7 sắc cầu vồng, nhưng không hề chói mắt, mà cực kỳ dịu và trendy.

Họa tiết kỳ lân ngộ nghĩnh khiến bộ đồ này như được bước ra từ thế giới cổ tích – cực kỳ hợp với những cô nàng “kẹo ngọt” chính hiệu.

👗 Chất vải & cảm giác mặc:
Vải thun cotton lạnh, mát da, mềm mịn, không bị xù lông hay bai dão sau khi giặt.

Form rộng vừa phải, mặc lên nhìn rất trẻ trung và năng động.

Dễ phối cùng dép bông, túi vải, hoặc cài tóc đáng yêu – biến bạn thành nàng kỳ lân bước xuống phố 🌈

✅ Phù hợp với:
Mặc nhà, đi siêu thị, cafe với bạn bè, hoặc thậm chí là ngủ cũng vẫn xinh.

Các bạn trẻ yêu phong cách Hàn – Nhật đáng yêu, muốn “auto nổi bật” dù chỉ đi dạo.

🎁 Ưu đãi xinh xẻo dành cho bạn:
👉 Mã KOC: UWiJ6eSyCS

💰 Giá trị mã: 0.02 (áp dụng khi mua hàng)

Đừng bỏ lỡ, vì kỳ lân này không chỉ bay mà còn “bay hàng” rất nhanh đó nha! 😍
Link sản phẩm:
http://127.0.0.1:5000/products/product/2', CAST(N'2025-04-23T22:08:17.323' AS DateTime), CAST(N'2025-04-23T22:37:57.840' AS DateTime))
GO
INSERT [dbo].[Reviews] ([id], [registerId], [rating], [text], [createdAt], [updatedAt]) VALUES (3, 12, 5, N'🌈✨ Review Đồ Bộ Kỳ Lân 7 Màu – Mặc Là “Auto Cute” ✨🌈
Nếu bạn đang cần tìm một bộ đồ vừa dễ thương, vừa thoải mái để mặc ở nhà hay đi chơi nhẹ nhàng thì... đồ bộ kỳ lân 7 màu là chân ái! 🦄💖

🧁 Ấn tượng đầu tiên:
Màu sắc rực rỡ 7 sắc cầu vồng, nhưng không hề chói mắt, mà cực kỳ dịu và trendy.

Họa tiết kỳ lân ngộ nghĩnh khiến bộ đồ này như được bước ra từ thế giới cổ tích – cực kỳ hợp với những cô nàng “kẹo ngọt” chính hiệu.

👗 Chất vải & cảm giác mặc:
Vải thun cotton lạnh, mát da, mềm mịn, không bị xù lông hay bai dão sau khi giặt.

Form rộng vừa phải, mặc lên nhìn rất trẻ trung và năng động.

Dễ phối cùng dép bông, túi vải, hoặc cài tóc đáng yêu – biến bạn thành nàng kỳ lân bước xuống phố 🌈

✅ Phù hợp với:
Mặc nhà, đi siêu thị, cafe với bạn bè, hoặc thậm chí là ngủ cũng vẫn xinh.

Các bạn trẻ yêu phong cách Hàn – Nhật đáng yêu, muốn “auto nổi bật” dù chỉ đi dạo.

🎁 Ưu đãi xinh xẻo dành cho bạn:
👉 Mã KOC: UWiJ6eSyCS

💰 Giá trị mã: 0.02 (áp dụng khi mua hàng)

Đừng bỏ lỡ, vì kỳ lân này không chỉ bay mà còn “bay hàng” rất nhanh đó nha! 😍
Link sản phẩm:
http://127.0.0.1:5000/products/product/2', CAST(N'2025-04-23T22:55:37.467' AS DateTime), CAST(N'2025-04-23T22:55:37.467' AS DateTime))
GO
INSERT [dbo].[Reviews] ([id], [registerId], [rating], [text], [createdAt], [updatedAt]) VALUES (4, 14, 5, N'Tuyệt vời.
Hãy mua nó', CAST(N'2025-04-24T09:19:16.870' AS DateTime), CAST(N'2025-04-24T09:19:16.870' AS DateTime))
GO
SET IDENTITY_INSERT [dbo].[Reviews] OFF
GO
SET IDENTITY_INSERT [dbo].[role] ON 
GO
INSERT [dbo].[role] ([id], [name], [description]) VALUES (1, N'Nhân viên', NULL)
GO
INSERT [dbo].[role] ([id], [name], [description]) VALUES (2, N'KOC', NULL)
GO
INSERT [dbo].[role] ([id], [name], [description]) VALUES (3, N'Người dùng thông thường', NULL)
GO
INSERT [dbo].[role] ([id], [name], [description]) VALUES (4, N'Doanh nghiệp', NULL)
GO
INSERT [dbo].[role] ([id], [name], [description]) VALUES (5, N'Admin', NULL)
GO
SET IDENTITY_INSERT [dbo].[role] OFF
GO
INSERT [dbo].[User] ([userName], [password], [roleId], [createdAt], [updatedAt], [authenticate], [status]) VALUES (N'doanhnghiep1                    ', N'123456                                                          ', 4, CAST(N'2025-04-08T08:12:49.523' AS DateTime), CAST(N'2025-04-21T02:38:24.633' AS DateTime), 1, N'hoạt động')
GO
INSERT [dbo].[User] ([userName], [password], [roleId], [createdAt], [updatedAt], [authenticate], [status]) VALUES (N'doanhnghiep5                    ', N'123456                                                          ', 4, CAST(N'2025-04-18T02:17:26.560' AS DateTime), CAST(N'2025-04-23T11:11:43.467' AS DateTime), 1, N'hoạt động')
GO
INSERT [dbo].[User] ([userName], [password], [roleId], [createdAt], [updatedAt], [authenticate], [status]) VALUES (N'nguoitieudung02                 ', N'123456                                                          ', 2, CAST(N'2025-04-23T11:27:22.307' AS DateTime), CAST(N'2025-04-23T11:27:27.633' AS DateTime), 1, N'hoạt động')
GO
INSERT [dbo].[User] ([userName], [password], [roleId], [createdAt], [updatedAt], [authenticate], [status]) VALUES (N'nguoitieudung03                 ', N'123456                                                          ', 2, CAST(N'2025-04-24T06:20:09.240' AS DateTime), CAST(N'2025-04-24T06:24:13.480' AS DateTime), 1, N'hoạt động')
GO
INSERT [dbo].[User] ([userName], [password], [roleId], [createdAt], [updatedAt], [authenticate], [status]) VALUES (N'nguoitieudung04                 ', N'123456                                                          ', 3, CAST(N'2025-04-24T08:58:08.427' AS DateTime), CAST(N'2025-04-24T08:58:08.427' AS DateTime), 0, N'Chờ')
GO
INSERT [dbo].[User] ([userName], [password], [roleId], [createdAt], [updatedAt], [authenticate], [status]) VALUES (N'nguoitieudung05                 ', N'123456                                                          ', 2, CAST(N'2025-04-24T09:01:02.043' AS DateTime), CAST(N'2025-04-24T09:04:38.373' AS DateTime), 1, N'hoạt động')
GO
INSERT [dbo].[User] ([userName], [password], [roleId], [createdAt], [updatedAt], [authenticate], [status]) VALUES (N'nhanvien1                       ', N'1234567                                                         ', 1, CAST(N'2025-01-01T00:00:00.000' AS DateTime), CAST(N'2025-04-24T09:05:40.000' AS DateTime), 1, N'hoạt động')
GO
INSERT [dbo].[User] ([userName], [password], [roleId], [createdAt], [updatedAt], [authenticate], [status]) VALUES (N'pakamon                         ', N'123211                                                          ', 2, CAST(N'2025-04-08T08:08:25.983' AS DateTime), CAST(N'2025-04-08T08:08:25.983' AS DateTime), 1, N'hoạt động')
GO
ALTER TABLE [dbo].[business] ADD  CONSTRAINT [DF_business_authenticate]  DEFAULT ((0)) FOR [authenticate]
GO
ALTER TABLE [dbo].[campaign] ADD  CONSTRAINT [DF_campaign_status]  DEFAULT ((0)) FOR [status]
GO
ALTER TABLE [dbo].[koc] ADD  CONSTRAINT [DF_koc_isKoc]  DEFAULT ((0)) FOR [isKoc]
GO
ALTER TABLE [dbo].[orderPro] ADD  CONSTRAINT [DF_orderPro_isPay]  DEFAULT ((0)) FOR [isPay]
GO
ALTER TABLE [dbo].[business]  WITH CHECK ADD  CONSTRAINT [FK_business_User] FOREIGN KEY([userId])
REFERENCES [dbo].[User] ([userName])
GO
ALTER TABLE [dbo].[business] CHECK CONSTRAINT [FK_business_User]
GO
ALTER TABLE [dbo].[campaign]  WITH CHECK ADD  CONSTRAINT [FK_Campaign_Admin] FOREIGN KEY([isConfirmed])
REFERENCES [dbo].[employee] ([id])
ON UPDATE CASCADE
ON DELETE CASCADE
GO
ALTER TABLE [dbo].[campaign] CHECK CONSTRAINT [FK_Campaign_Admin]
GO
ALTER TABLE [dbo].[campaign]  WITH CHECK ADD  CONSTRAINT [FK_Campaign_Adviser] FOREIGN KEY([businessId])
REFERENCES [dbo].[business] ([id])
ON UPDATE CASCADE
ON DELETE CASCADE
GO
ALTER TABLE [dbo].[campaign] CHECK CONSTRAINT [FK_Campaign_Adviser]
GO
ALTER TABLE [dbo].[campaign]  WITH CHECK ADD  CONSTRAINT [FK_Campaign_Campaign_category] FOREIGN KEY([campaignCategoryId])
REFERENCES [dbo].[campaignCategory] ([id])
ON UPDATE CASCADE
ON DELETE CASCADE
GO
ALTER TABLE [dbo].[campaign] CHECK CONSTRAINT [FK_Campaign_Campaign_category]
GO
ALTER TABLE [dbo].[campaignProduct]  WITH CHECK ADD  CONSTRAINT [FK_Campaign_product_Campaign] FOREIGN KEY([campaignId])
REFERENCES [dbo].[campaign] ([id])
ON UPDATE CASCADE
ON DELETE CASCADE
GO
ALTER TABLE [dbo].[campaignProduct] CHECK CONSTRAINT [FK_Campaign_product_Campaign]
GO
ALTER TABLE [dbo].[campaignProduct]  WITH CHECK ADD  CONSTRAINT [FK_campaignProduct_productBusinees] FOREIGN KEY([productId])
REFERENCES [dbo].[productBusinees] ([id])
GO
ALTER TABLE [dbo].[campaignProduct] CHECK CONSTRAINT [FK_campaignProduct_productBusinees]
GO
ALTER TABLE [dbo].[commission]  WITH CHECK ADD  CONSTRAINT [FK_Commission_Register_campaign] FOREIGN KEY([registerId])
REFERENCES [dbo].[registerCampaign] ([id])
ON UPDATE CASCADE
ON DELETE CASCADE
GO
ALTER TABLE [dbo].[commission] CHECK CONSTRAINT [FK_Commission_Register_campaign]
GO
ALTER TABLE [dbo].[employee]  WITH CHECK ADD  CONSTRAINT [FK_Admin_User] FOREIGN KEY([userId])
REFERENCES [dbo].[User] ([userName])
GO
ALTER TABLE [dbo].[employee] CHECK CONSTRAINT [FK_Admin_User]
GO
ALTER TABLE [dbo].[koc]  WITH CHECK ADD  CONSTRAINT [FK_KOC_User] FOREIGN KEY([userId])
REFERENCES [dbo].[User] ([userName])
ON UPDATE CASCADE
ON DELETE CASCADE
GO
ALTER TABLE [dbo].[koc] CHECK CONSTRAINT [FK_KOC_User]
GO
ALTER TABLE [dbo].[orderDetail]  WITH CHECK ADD  CONSTRAINT [FK_orderDetail_orderPro] FOREIGN KEY([orderId])
REFERENCES [dbo].[orderPro] ([id])
GO
ALTER TABLE [dbo].[orderDetail] CHECK CONSTRAINT [FK_orderDetail_orderPro]
GO
ALTER TABLE [dbo].[orderDetail]  WITH CHECK ADD  CONSTRAINT [FK_orderDetail_productBusinees] FOREIGN KEY([productId])
REFERENCES [dbo].[productBusinees] ([id])
ON UPDATE CASCADE
ON DELETE CASCADE
GO
ALTER TABLE [dbo].[orderDetail] CHECK CONSTRAINT [FK_orderDetail_productBusinees]
GO
ALTER TABLE [dbo].[orderPro]  WITH CHECK ADD  CONSTRAINT [FK_orderPro_koc] FOREIGN KEY([kocId])
REFERENCES [dbo].[koc] ([id])
GO
ALTER TABLE [dbo].[orderPro] CHECK CONSTRAINT [FK_orderPro_koc]
GO
ALTER TABLE [dbo].[proCate]  WITH CHECK ADD  CONSTRAINT [FK_Pro_cate_Product] FOREIGN KEY([productId])
REFERENCES [dbo].[product] ([id])
ON UPDATE CASCADE
ON DELETE CASCADE
GO
ALTER TABLE [dbo].[proCate] CHECK CONSTRAINT [FK_Pro_cate_Product]
GO
ALTER TABLE [dbo].[proCate]  WITH CHECK ADD  CONSTRAINT [FK_Pro_cate_Product_category] FOREIGN KEY([productCategoryId])
REFERENCES [dbo].[productCategory] ([id])
ON UPDATE CASCADE
ON DELETE CASCADE
GO
ALTER TABLE [dbo].[proCate] CHECK CONSTRAINT [FK_Pro_cate_Product_category]
GO
ALTER TABLE [dbo].[productBusinees]  WITH CHECK ADD  CONSTRAINT [FK_productBusinees_business] FOREIGN KEY([businessId])
REFERENCES [dbo].[business] ([id])
ON UPDATE CASCADE
ON DELETE CASCADE
GO
ALTER TABLE [dbo].[productBusinees] CHECK CONSTRAINT [FK_productBusinees_business]
GO
ALTER TABLE [dbo].[productBusinees]  WITH CHECK ADD  CONSTRAINT [FK_productBusinees_product] FOREIGN KEY([productId])
REFERENCES [dbo].[product] ([id])
ON UPDATE CASCADE
ON DELETE CASCADE
GO
ALTER TABLE [dbo].[productBusinees] CHECK CONSTRAINT [FK_productBusinees_product]
GO
ALTER TABLE [dbo].[registerCampaign]  WITH CHECK ADD  CONSTRAINT [FK_Register_campaign_Campaign_product1] FOREIGN KEY([campaign_product_id])
REFERENCES [dbo].[campaignProduct] ([id])
ON UPDATE CASCADE
ON DELETE CASCADE
GO
ALTER TABLE [dbo].[registerCampaign] CHECK CONSTRAINT [FK_Register_campaign_Campaign_product1]
GO
ALTER TABLE [dbo].[registerCampaign]  WITH CHECK ADD  CONSTRAINT [FK_Register_campaign_KOC1] FOREIGN KEY([kocId])
REFERENCES [dbo].[koc] ([id])
ON UPDATE CASCADE
ON DELETE CASCADE
GO
ALTER TABLE [dbo].[registerCampaign] CHECK CONSTRAINT [FK_Register_campaign_KOC1]
GO
ALTER TABLE [dbo].[reviewDetails]  WITH CHECK ADD  CONSTRAINT [FK_reviewDetails_koc] FOREIGN KEY([kocId])
REFERENCES [dbo].[koc] ([id])
ON UPDATE CASCADE
ON DELETE CASCADE
GO
ALTER TABLE [dbo].[reviewDetails] CHECK CONSTRAINT [FK_reviewDetails_koc]
GO
ALTER TABLE [dbo].[reviewDetails]  WITH CHECK ADD  CONSTRAINT [FK_reviewDetails_Reviews] FOREIGN KEY([reviewId])
REFERENCES [dbo].[Reviews] ([id])
GO
ALTER TABLE [dbo].[reviewDetails] CHECK CONSTRAINT [FK_reviewDetails_Reviews]
GO
ALTER TABLE [dbo].[Reviews]  WITH CHECK ADD  CONSTRAINT [FK_Reviews_Register_campaign] FOREIGN KEY([registerId])
REFERENCES [dbo].[registerCampaign] ([id])
ON UPDATE CASCADE
ON DELETE CASCADE
GO
ALTER TABLE [dbo].[Reviews] CHECK CONSTRAINT [FK_Reviews_Register_campaign]
GO
ALTER TABLE [dbo].[roleDetails]  WITH CHECK ADD  CONSTRAINT [FK_roleDetails_role1] FOREIGN KEY([roleId])
REFERENCES [dbo].[role] ([id])
GO
ALTER TABLE [dbo].[roleDetails] CHECK CONSTRAINT [FK_roleDetails_role1]
GO
ALTER TABLE [dbo].[roleDetails]  WITH CHECK ADD  CONSTRAINT [FK_roleDetails_roleFunction] FOREIGN KEY([functionId])
REFERENCES [dbo].[roleFunction] ([id])
GO
ALTER TABLE [dbo].[roleDetails] CHECK CONSTRAINT [FK_roleDetails_roleFunction]
GO
ALTER TABLE [dbo].[User]  WITH CHECK ADD  CONSTRAINT [FK_User_Role] FOREIGN KEY([roleId])
REFERENCES [dbo].[role] ([id])
ON DELETE CASCADE
GO
ALTER TABLE [dbo].[User] CHECK CONSTRAINT [FK_User_Role]
GO
