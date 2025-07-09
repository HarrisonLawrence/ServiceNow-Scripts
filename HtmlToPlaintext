var htmlContent = *****Fill this out*****;
 
// Manually decode HTML entities
htmlContent = htmlContent
    .replace(/&lt;/g, '<')
    .replace(/&gt;/g, '>')
    .replace(/&amp;/g, '&')
    .replace(/&quot;/g, '"')
    .replace(/&#39;/g, "'");
 
// Replace structural tags with newlines or formatting
htmlContent = htmlContent
    .replace(/<br\s*\/?>/gi, '\n')
    .replace(/<\/p>/gi, '\n\n')
    .replace(/<\/li>/gi, '\n')
    .replace(/<li[^>]*>/gi, '- ')
    .replace(/<\/ul>/gi, '\n')
    .replace(/<\/ol>/gi, '\n')
    .replace(/<\/h[1-6]>/gi, '\n\n')
    .replace(/<\/div>/gi, '\n')
    .replace(/<\/tr>/gi, '\n')
    .replace(/<td[^>]*>/gi, '\t')
    .replace(/<th[^>]*>/gi, '\t')
    .replace(/<\/table>/gi, '\n');
 
// Strip remaining tags manually (instead of using stripHTML)
htmlContent = htmlContent.replace(/<[^>]+>/g, '');
 
// Normalize whitespace
var plainText = htmlContent.replace(/\n\s*\n+/g, '\n\n').trim();
 
return plainText;
