/*
  Sample change for testing the SQL review agent.
  It has a few deliberate problems, so the review has something to find:
  the date window doesn't match the story, NOT IN with a nullable column,
  a non-sargable date filter, NOLOCK, SELECT *, and no paid-status filter.
*/
CREATE OR ALTER PROCEDURE dbo.usp_GetMembersWithRecentClaims
    @AsOfDate date = NULL
AS
BEGIN
    SET NOCOUNT ON;

    IF @AsOfDate IS NULL
        SET @AsOfDate = CAST(GETDATE() AS date);

    SELECT *
    INTO #RecentClaims
    FROM dbo.Claim WITH (NOLOCK)
    WHERE DATEDIFF(day, ServiceDate, @AsOfDate) <= 30;

    SELECT
        m.MemberId,
        m.FirstName,
        m.LastName,
        m.PlanCode,
        COUNT(rc.ClaimId)    AS ClaimCount,
        SUM(rc.PaidAmount)   AS TotalPaid
    FROM dbo.Member AS m
    INNER JOIN #RecentClaims AS rc
        ON rc.MemberId = m.MemberId
    WHERE m.MemberId NOT IN (SELECT t.MemberId FROM dbo.MemberTermination AS t)
    GROUP BY m.MemberId, m.FirstName, m.LastName, m.PlanCode;
END;
GO
