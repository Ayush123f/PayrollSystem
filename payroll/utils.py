from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from django.http import HttpResponse


def generate_payslip_pdf(payroll):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = (
        f'attachment; filename="payslip_{payroll.employee.employee_id}'
        f'_{payroll.month}_{payroll.year}.pdf"'
    )

    c = canvas.Canvas(response, pagesize=A4)
    width, height = A4

    # ── Header Background ─────────────────────
    c.setFillColor(colors.HexColor('#1a1a2e'))
    c.rect(0, height - 120, width, 120, fill=True, stroke=False)

    # ── Company Name ──────────────────────────
    c.setFillColor(colors.white)
    c.setFont('Helvetica-Bold', 20)
    c.drawString(50, height - 50, 'PayrollPro Inc.')

    c.setFont('Helvetica', 11)
    c.drawString(50, height - 70, 'Kathmandu, Nepal')

    c.setFont('Helvetica-Bold', 13)
    c.drawString(50, height - 100, f'Salary Payslip - {payroll.get_month_display()} {payroll.year}')

    # ── Payslip Number ────────────────────────
    c.setFont('Helvetica', 10)
    c.drawString(400, height - 50, f'Payslip No: PSL-{payroll.year}-{payroll.pk:04d}')
    c.drawString(400, height - 65, f'Status: {payroll.get_status_display()}')

    # ── Employee Info ─────────────────────────
    c.setFillColor(colors.HexColor('#1a1a2e'))
    c.setFont('Helvetica-Bold', 12)
    c.drawString(50, height - 160, 'Employee Information')

    c.setFont('Helvetica', 11)
    c.drawString(50,  height - 180, f'Name:       {payroll.employee.user.get_full_name()}')
    c.drawString(50,  height - 198, f'ID:         {payroll.employee.employee_id}')
    c.drawString(50,  height - 216, f'Department: {payroll.employee.department.name if payroll.employee.department else "N/A"}')
    c.drawString(300, height - 180, f'Type:       {payroll.employee.get_employee_type_display()}')
    c.drawString(300, height - 198, f'Month:      {payroll.get_month_display()} {payroll.year}')

    # ── Divider ───────────────────────────────
    c.setStrokeColor(colors.HexColor('#e6e8f0'))
    c.line(50, height - 235, width - 50, height - 235)

    # ── Earnings ──────────────────────────────
    c.setFillColor(colors.HexColor('#1a1a2e'))
    c.setFont('Helvetica-Bold', 12)
    c.drawString(50, height - 260, 'Earnings')

    c.setFont('Helvetica', 11)
    y = height - 280
    c.drawString(50,  y, 'Basic Salary')
    c.drawString(300, y, f'Rs. {payroll.salary_structure.basic_salary:,.2f}')
    y -= 18
    c.drawString(50,  y, 'House Rent Allowance (HRA)')
    c.drawString(300, y, f'Rs. {payroll.salary_structure.hra:,.2f}')
    y -= 18
    c.drawString(50,  y, 'Other Allowances')
    c.drawString(300, y, f'Rs. {payroll.salary_structure.allowances:,.2f}')
    if payroll.bonus:
        y -= 18
        c.drawString(50,  y, 'Bonus')
        c.drawString(300, y, f'Rs. {payroll.bonus:,.2f}')

    y -= 10
    c.line(50, y, width - 50, y)
    y -= 18
    c.setFont('Helvetica-Bold', 11)
    c.drawString(50,  y, 'Gross Salary')
    c.drawString(300, y, f'Rs. {payroll.gross_salary:,.2f}')

    # ── Deductions ────────────────────────────
    y -= 30
    c.setFont('Helvetica-Bold', 12)
    c.drawString(50, y, 'Deductions')

    c.setFont('Helvetica', 11)
    y -= 20
    c.drawString(50,  y, f'Income Tax ({payroll.salary_structure.tax_rate}%)')
    c.drawString(300, y, f'Rs. {payroll.tax_deduction:,.2f}')
    y -= 18
    c.drawString(50,  y, f'Provident Fund ({payroll.salary_structure.pf_percentage}%)')
    c.drawString(300, y, f'Rs. {payroll.pf_deduction:,.2f}')

    y -= 10
    c.line(50, y, width - 50, y)
    y -= 18
    c.setFont('Helvetica-Bold', 11)
    c.drawString(50,  y, 'Total Deductions')
    c.drawString(300, y, f'Rs. {payroll.total_deduction:,.2f}')

    # ── Net Pay Box ───────────────────────────
    y -= 40
    c.setFillColor(colors.HexColor('#f4f5f9'))
    c.rect(40, y - 10, width - 80, 45, fill=True, stroke=False)
    c.setFillColor(colors.HexColor('#1a1a2e'))
    c.setFont('Helvetica-Bold', 14)
    c.drawString(55, y + 18, 'NET PAY')
    c.drawString(300, y + 18, f'Rs. {payroll.net_salary:,.2f}')

    # ── Footer ────────────────────────────────
    c.setFont('Helvetica', 9)
    c.setFillColor(colors.HexColor('#7a7f9a'))
    c.drawString(50, 40, 'This is a computer-generated payslip. No signature required.')
    c.drawString(50, 25, 'For queries contact: hr@payrollpro.com')

    c.save()
    return response